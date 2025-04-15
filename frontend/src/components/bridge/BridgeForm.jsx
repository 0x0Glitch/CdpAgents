// src/components/bridge/BridgeForm.jsx
import React, { useState, useEffect } from 'react';
import { ChevronRight } from 'lucide-react';
import { NetworkSelector, AmountInput, AddressInput } from '../common/Inputs';
import { PrimaryButton } from '../common/Button';
import { FrostedCard } from '../common/Cards';
import web3Service from '../../services/web3Service';

const networkOptions = [
  { id: '84532', name: 'Base Sepolia' },
  { id: '11155420', name: 'Optimism Sepolia' },
  { id: '999', name: 'Zora Testnet' },
  { id: '80002', name: 'Unichain Testnet' }
];

const BridgeForm = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [account, setAccount] = useState('');
  const [currentChainId, setCurrentChainId] = useState('');
  const [sourceChainId, setSourceChainId] = useState('84532');
  const [targetChainId, setTargetChainId] = useState('11155420');
  const [amount, setAmount] = useState('');
  const [recipient, setRecipient] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [taskId, setTaskId] = useState('');
  const [taskStatus, setTaskStatus] = useState('');
  const [balances, setBalances] = useState({
    superUSDC: '0',
    usdc: '0'
  });

  // Connect wallet
  const connectWallet = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await web3Service.connect();
      
      if (response.success) {
        setIsConnected(true);
        setAccount(response.address);
        setCurrentChainId(response.chainId);
        setRecipient(response.address);
        
        // Load balances
        await loadBalances(response.chainId);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load balances
  const loadBalances = async (chainId) => {
    try {
      const response = await web3Service.getBalances(chainId);
      
      if (response.success) {
        setBalances(response.balances);
      } else {
        console.error('Failed to load balances:', response.error);
      }
    } catch (err) {
      console.error('Error loading balances:', err);
    }
  };

  // Switch network
  const switchNetwork = async (chainId) => {
    setLoading(true);
    setError('');
    
    try {
      const response = await web3Service.switchNetwork(chainId);
      
      if (response.success) {
        setCurrentChainId(response.chainId);
        await loadBalances(response.chainId);
      } else {
        setError(response.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle source chain change
  const handleSourceChainChange = (e) => {
    const newSourceChainId = e.target.value;
    setSourceChainId(newSourceChainId);
    
    // If target chain is the same as new source, switch target
    if (newSourceChainId === targetChainId) {
      // Find a different chain for target
      const differentChain = networkOptions.find(
        network => network.id !== newSourceChainId
      );
      
      if (differentChain) {
        setTargetChainId(differentChain.id);
      }
    }
  };

  // Handle target chain change
  const handleTargetChainChange = (e) => {
    const newTargetChainId = e.target.value;
    setTargetChainId(newTargetChainId);
    
    // If source chain is the same as new target, switch source
    if (sourceChainId === newTargetChainId) {
      // Find a different chain for source
      const differentChain = networkOptions.find(
        network => network.id !== newTargetChainId
      );
      
      if (differentChain) {
        setSourceChainId(differentChain.id);
      }
    }
  };

  // Handle bridge submission
  const handleBridge = async (e) => {
    e.preventDefault();
    
    if (!isConnected) {
      setError('Please connect your wallet first');
      return;
    }
    
    if (!amount || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount');
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccess('');
    setTaskId('');
    setTaskStatus('');
    
    try {
      // First switch to source chain if not already there
      if (currentChainId !== sourceChainId) {
        const switchResponse = await web3Service.switchNetwork(sourceChainId);
        
        if (!switchResponse.success) {
          throw new Error('Failed to switch to source chain');
        }
        
        setCurrentChainId(sourceChainId);
      }
      
      // Check if we have enough balance
      await loadBalances(sourceChainId);
      
      if (parseFloat(balances.superUSDC) < parseFloat(amount)) {
        throw new Error('Insufficient SuperUSDC balance on source chain');
      }
      
      // Call the cross-chain transfer
      const response = await web3Service.crossChainTransfer(
        amount,
        sourceChainId,
        targetChainId,
        recipient || account
      );
      
      if (response.success) {
        setTaskId(response.taskId);
        setTaskStatus(response.status);
        setSuccess(`Cross-chain transfer initiated! Task ID: ${response.taskId}`);
        
        // Start polling for task status
        startPollingTaskStatus(response.taskId);
      } else {
        throw new Error(response.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Start polling for task status
  const startPollingTaskStatus = (taskId) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await web3Service.checkTransferStatus(taskId);
        
        if (response.success) {
          setTaskStatus(response.status);
          
          if (response.status === 'completed') {
            setSuccess('Cross-chain transfer completed successfully!');
            clearInterval(pollInterval);
            
            // Reload balances for both chains
            await loadBalances(sourceChainId);
            
            // Switch to target chain and load balances
            await web3Service.switchNetwork(targetChainId);
            await loadBalances(targetChainId);
          } else if (response.status === 'failed') {
            setError(`Cross-chain transfer failed: ${response.error}`);
            clearInterval(pollInterval);
          }
        }
      } catch (err) {
        console.error('Error checking task status:', err);
      }
    }, 5000); // Poll every 5 seconds
    
    // Clear interval after 2 minutes
    setTimeout(() => {
      clearInterval(pollInterval);
    }, 120000);
  };

  // Handle deposit to get SuperUSDC
  const handleDeposit = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount');
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      // Make sure we're on the right chain
      if (currentChainId !== sourceChainId) {
        await switchNetwork(sourceChainId);
      }
      
      // Check if we have enough USDC
      if (parseFloat(balances.usdc) < parseFloat(amount)) {
        throw new Error('Insufficient USDC balance');
      }
      
      // Perform deposit
      const response = await web3Service.deposit(amount, sourceChainId);
      
      if (response.success) {
        setSuccess(`Deposit successful! Transaction hash: ${response.txHash}`);
        await loadBalances(sourceChainId);
      } else {
        throw new Error(response.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle withdrawal to get USDC back
  const handleWithdraw = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount');
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      // Make sure we're on the right chain
      if (currentChainId !== sourceChainId) {
        await switchNetwork(sourceChainId);
      }
      
      // Check if we have enough SuperUSDC
      if (parseFloat(balances.superUSDC) < parseFloat(amount)) {
        throw new Error('Insufficient SuperUSDC balance');
      }
      
      // Perform withdrawal
      const response = await web3Service.withdraw(amount, sourceChainId);
      
      if (response.success) {
        setSuccess(`Withdrawal successful! Transaction hash: ${response.txHash}`);
        await loadBalances(sourceChainId);
      } else {
        throw new Error(response.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Listen for account or chain changes
  useEffect(() => {
    if (window.ethereum) {
      window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length > 0) {
          setAccount(accounts[0]);
          setRecipient(accounts[0]);
        } else {
          setIsConnected(false);
          setAccount('');
        }
      });
      
      window.ethereum.on('chainChanged', (chainId) => {
        setCurrentChainId(parseInt(chainId, 16).toString());
        loadBalances(parseInt(chainId, 16).toString());
      });
    }
    
    return () => {
      if (window.ethereum) {
        window.ethereum.removeAllListeners('accountsChanged');
        window.ethereum.removeAllListeners('chainChanged');
      }
    };
  }, []);

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-center mb-6">Skywire Cross-Chain Bridge</h2>
      
      {/* Connection Status */}
      <div className="mb-6">
        {!isConnected ? (
          <button
            onClick={connectWallet}
            disabled={loading}
            className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-blue-300"
          >
            {loading ? 'Connecting...' : 'Connect Wallet'}
          </button>
        ) : (
          <div className="flex justify-between items-center">
            <div>
              <p className="text-sm">Connected: {account?.slice(0, 6)}...{account?.slice(-4)}</p>
              <p className="text-sm">
                Network: {networkOptions.find(n => n.id === currentChainId)?.name || currentChainId}
              </p>
            </div>
            <button
              onClick={() => switchNetwork(sourceChainId)}
              disabled={loading || currentChainId === sourceChainId}
              className="py-1 px-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 disabled:bg-gray-100 text-sm"
            >
              Switch to Source
            </button>
          </div>
        )}
      </div>
      
      {/* Bridge Form */}
      <form onSubmit={handleBridge}>
        {/* Source Chain */}
        <div className="mb-4">
          <label htmlFor="sourceChain" className="block text-sm font-medium text-gray-700">
            Source Chain
          </label>
          <select
            id="sourceChain"
            value={sourceChainId}
            onChange={handleSourceChainChange}
            disabled={loading}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            {networkOptions.map(network => (
              <option key={network.id} value={network.id}>
                {network.name}
              </option>
            ))}
          </select>
          {isConnected && (
            <div className="mt-1 flex justify-between text-sm">
              <span>SuperUSDC: {parseFloat(balances.superUSDC).toFixed(6)}</span>
              <span>USDC: {parseFloat(balances.usdc).toFixed(6)}</span>
            </div>
          )}
        </div>
        
        {/* Target Chain */}
        <div className="mb-4">
          <label htmlFor="targetChain" className="block text-sm font-medium text-gray-700">
            Target Chain
          </label>
          <select
            id="targetChain"
            value={targetChainId}
            onChange={handleTargetChainChange}
            disabled={loading}
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            {networkOptions.map(network => (
              <option key={network.id} value={network.id}>
                {network.name}
              </option>
            ))}
          </select>
        </div>
        
        {/* Amount */}
        <div className="mb-4">
          <label htmlFor="amount" className="block text-sm font-medium text-gray-700">
            Amount
          </label>
          <input
            id="amount"
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            disabled={loading}
            placeholder="0.00"
            min="0"
            step="0.000001"
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        {/* Recipient */}
        <div className="mb-6">
          <label htmlFor="recipient" className="block text-sm font-medium text-gray-700">
            Recipient (Optional - defaults to your address)
          </label>
          <input
            id="recipient"
            type="text"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            disabled={loading}
            placeholder="0x..."
            className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        
        {/* Action Buttons */}
        <div className="flex space-x-2 mb-4">
          <button
            type="button"
            onClick={handleDeposit}
            disabled={loading || !isConnected}
            className="flex-1 py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-green-300"
          >
            Deposit USDC
          </button>
          <button
            type="button"
            onClick={handleWithdraw}
            disabled={loading || !isConnected}
            className="flex-1 py-2 px-4 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:bg-red-300"
          >
            Withdraw USDC
          </button>
        </div>
        
        {/* Bridge Button */}
        <button
          type="submit"
          disabled={loading || !isConnected}
          className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:bg-indigo-300"
        >
          {loading ? 'Processing...' : 'Bridge SuperUSDC'}
        </button>
        
        {/* Error & Success Messages */}
        {error && (
          <div className="mt-4 p-2 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}
        {success && (
          <div className="mt-4 p-2 bg-green-100 text-green-700 rounded-md">
            {success}
          </div>
        )}
        
        {/* Task Status */}
        {taskId && (
          <div className="mt-4 p-2 bg-blue-50 rounded-md">
            <p className="text-sm">
              <span className="font-medium">Task ID:</span> {taskId}
            </p>
            <p className="text-sm">
              <span className="font-medium">Status:</span> {taskStatus}
            </p>
          </div>
        )}
      </form>
    </div>
  );
};

export default BridgeForm;