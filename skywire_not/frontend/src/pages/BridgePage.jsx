// src/pages/BridgePage.jsx
import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { NavLink } from 'react-router-dom';
import { ArrowLeftRight, Activity } from 'lucide-react';
import Logo from '../components/common/Logo';
import BridgeBackground from '../components/common/BridgeBackground';
import { TabButton } from '../components/common/Inputs';
import ActionSelector from '../components/bridge/ActionSelector';
import BridgeForm from '../components/bridge/BridgeForm';
import DepositForm from '../components/bridge/DepositForm';
import WithdrawForm from '../components/bridge/WithdrawForm';
import StatusDisplay from '../components/bridge/StatusDisplay';
import BalanceDisplay from '../components/bridge/BalanceDisplay';
import NetworkStats from '../components/bridge/NetworkStats';
import WalletButton from '../components/bridge/ConnectButton';
import { SUPERETH_ABI, CONTRACT_ADDRESS, SUPPORTED_CHAINS } from '../components/constants/chain';

const BridgePage = () => {
  // State variables
  const [provider, setProvider] = useState(null);
  const [signer, setSigner] = useState(null);
  const [currentChainId, setCurrentChainId] = useState(null);
  const [userAddress, setUserAddress] = useState("");
  const [superEthBalance, setSuperEthBalance] = useState("0");
  const [depositAmount, setDepositAmount] = useState("");
  const [withdrawAmount, setWithdrawAmount] = useState("");
  const [bridgeAmount, setBridgeAmount] = useState("");
  const [bridgeSourceChain, setBridgeSourceChain] = useState(SUPPORTED_CHAINS[0]);
  const [bridgeTargetChain, setBridgeTargetChain] = useState(SUPPORTED_CHAINS[1]);
  const [bridgeRecipient, setBridgeRecipient] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [activeTab, setActiveTab] = useState('bridge');
  const [activeAction, setActiveAction] = useState('bridge');
  const [ethBalance, setEthBalance] = useState("0");

  // Effect for wallet connection and chain changes
  useEffect(() => {
    if (window.ethereum) {
      window.ethereum.on('chainChanged', (chainId) => {
        setCurrentChainId(chainId);
        resetContractData();
      });

      window.ethereum.on('accountsChanged', (accounts) => {
        if (accounts.length > 0) {
          setUserAddress(accounts[0]);
        } else {
          setUserAddress("");
        }
        resetContractData();
      });
    }
    return () => {
      if (window.ethereum) {
        window.ethereum.removeAllListeners('chainChanged');
        window.ethereum.removeAllListeners('accountsChanged');
      }
    };
  }, []);

  // Effect for loading balance
  useEffect(() => {
    if (userAddress && currentChainId && signer) {
      loadSuperETHBalance();
    }
  }, [userAddress, currentChainId, signer]);

  useEffect(() => {
    if (provider && userAddress) {
      loadEthBalance();
    }
  }, [provider, userAddress]);

  // Wallet connection
  async function connectWallet() {
    if (!window.ethereum) {
      alert("Please install Metamask or a compatible wallet.");
      return;
    }
    try {
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts'
      });
      const account = accounts[0];
      setUserAddress(account);

      const chainId = await window.ethereum.request({ method: 'eth_chainId' });
      setCurrentChainId(chainId);

      const newProvider = new ethers.BrowserProvider(window.ethereum);
      setProvider(newProvider);

      const newSigner = await newProvider.getSigner();
      setSigner(newSigner);

    } catch (err) {
      console.error("Error connecting wallet:", err);
    }
  }

  function resetContractData() {
    setSuperEthBalance("0");
    setStatusMessage("");
  }

  function getSuperETHContract() {
    if (!signer) return null;
    return new ethers.Contract(CONTRACT_ADDRESS, SUPERETH_ABI, signer);
  }

  async function loadSuperETHBalance() {
    try {
      setStatusMessage("Loading SuperETH balance...");
      const contract = getSuperETHContract();
      if (!contract) {
        setStatusMessage("No contract instance (signer not ready).");
        return;
      }
      const balance = await contract.balanceOf(userAddress);
      const decimals = await contract.decimals();
      const formatted = ethers.formatUnits(balance, decimals);
      setSuperEthBalance(formatted);
      setStatusMessage("SuperETH balance updated.");
    } catch (err) {
      console.error("Error loading balance:", err);
      setStatusMessage("Failed to load SuperETH balance.");
    }
  }

  async function loadEthBalance() {
    if (!provider || !userAddress) return;
    try {
      const balance = await provider.getBalance(userAddress);
      const formatted = ethers.formatEther(balance);
      setEthBalance(formatted);
    } catch (err) {
      console.error("Error loading ETH balance:", err);
    }
  }

  async function handleDeposit() {
    if (!depositAmount || Number(depositAmount) <= 0) {
      alert("Please enter a valid deposit amount.");
      return;
    }
    setStatusMessage("Depositing...");
    try {
      const contract = getSuperETHContract();
      if (!contract) {
        setStatusMessage("Signer or contract not available.");
        return;
      }
      const tx = await contract.deposit({
        value: ethers.parseEther(depositAmount)
      });
      await tx.wait();
      setStatusMessage("Deposit successful!");
      setDepositAmount("");
      loadSuperETHBalance();
      loadEthBalance();
    } catch (err) {
      console.error("Deposit error:", err);
      setStatusMessage("Deposit failed. See console for details.");
    }
  }

  async function handleWithdraw() {
    if (!withdrawAmount || Number(withdrawAmount) <= 0) {
      alert("Please enter a valid withdraw amount.");
      return;
    }
    setStatusMessage("Withdrawing...");
    try {
      const contract = getSuperETHContract();
      if (!contract) {
        setStatusMessage("Signer or contract not available.");
        return;
      }
      const decimals = await contract.decimals();
      const amountBig = ethers.parseUnits(withdrawAmount, decimals);

      const tx = await contract.withdraw(amountBig);
      await tx.wait();

      setStatusMessage("Withdraw successful!");
      setWithdrawAmount("");
      loadSuperETHBalance();
      loadEthBalance();
    } catch (err) {
      console.error("Withdraw error:", err);
      setStatusMessage("Withdraw failed. See console for details.");
    }
  }

  async function handleBridge() {
    if (!bridgeAmount || Number(bridgeAmount) <= 0) {
      alert("Please enter a valid bridging amount.");
      return;
    }
    if (!bridgeRecipient) {
      alert("Please enter a valid recipient address.");
      return;
    }
  
    setStatusMessage("Starting bridging operation...");
  
    await switchNetwork(bridgeSourceChain.chainId);
    const contractSource = getSuperETHContract();
    const decimals = await contractSource.decimals();
    const burnAmount = ethers.parseUnits(bridgeAmount, decimals);
  
    setStatusMessage(`Burning on source chain ${bridgeSourceChain.chainName}...`);
    try {
      const txBurn = await contractSource.crosschainBurn(userAddress, burnAmount);
      await txBurn.wait();
      setStatusMessage("Burn on source chain successful!");
      
      // Show minting message after burn is successful
      setTimeout(() => {
        setStatusMessage(`Minting on target chain ${bridgeTargetChain.chainName}...`);
        
        // After 5 seconds of showing the minting message, load the balances
        setTimeout(async () => {
          await loadSuperETHBalance();
          await loadEthBalance();
        }, 5000);
        
      }, 2000); // Short delay after burn success message
      
    } catch (err) {
      console.error("crosschainBurn error:", err);
      setStatusMessage("Burn failed (likely not authorized).");
      return;
    }
  }

  async function switchNetwork(chainIdHex) {
    if (!window.ethereum) {
      alert("No wallet found to switch network");
      return;
    }
    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: chainIdHex }]
      });
    } catch (switchError) {
      console.error(switchError);
    }
  }

  return (
    <div className="min-h-screen text-white">
      {/* Custom background for bridge page */}
      <BridgeBackground />
      
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md my-5 mb-2bg-slate-950/30 border-b border-white/5">
        <div className="container mx-auto px-6 h-20">
          <div className="flex items-center justify-between h-full">
            <div className="flex items-center space-x-8">
              <NavLink to="/" className="flex items-center space-x-3">
                <Logo />
              </NavLink>
              
              <nav className="hidden md:flex space-x-2">
                <TabButton
                  active={activeTab === 'bridge'}
                  onClick={() => setActiveTab('bridge')}
                  icon={ArrowLeftRight}
                  label="Bridge"
                />
                <TabButton
                  active={activeTab === 'activity'}
                  onClick={() => setActiveTab('activity')}
                  icon={Activity}
                  label="Activity"
                />
              </nav>
            </div>

            <WalletButton 
              userAddress={userAddress}
              connectWallet={connectWallet}
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 pt-32 pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Form Section */}
          <div className="lg:col-span-2 space-y-8">
            {/* Action Selection */}
            <ActionSelector 
              activeAction={activeAction} 
              setActiveAction={setActiveAction}
            />

            {/* Form Content based on active action */}
            {activeAction === 'bridge' && (
              <BridgeForm
                bridgeAmount={bridgeAmount}
                setBridgeAmount={setBridgeAmount}
                bridgeSourceChain={bridgeSourceChain}
                setBridgeSourceChain={setBridgeSourceChain}
                bridgeTargetChain={bridgeTargetChain}
                setBridgeTargetChain={setBridgeTargetChain}
                bridgeRecipient={bridgeRecipient}
                setBridgeRecipient={setBridgeRecipient}
                handleBridge={handleBridge}
                supportedChains={SUPPORTED_CHAINS}
                disabled={!userAddress}
              />
            )}

            {activeAction === 'deposit' && (
              <DepositForm
                depositAmount={depositAmount}
                setDepositAmount={setDepositAmount}
                handleDeposit={handleDeposit}
                disabled={!userAddress}
              />
            )}

            {activeAction === 'withdraw' && (
              <WithdrawForm
                withdrawAmount={withdrawAmount}
                setWithdrawAmount={setWithdrawAmount}
                handleWithdraw={handleWithdraw}
                disabled={!userAddress}
              />
            )}

            {/* Status Messages */}
            <StatusDisplay statusMessage={statusMessage} />
          </div>

          {/* Side Panel */}
          <div className="space-y-8">
            {/* Balances Card */}
            <BalanceDisplay
              ethBalance={ethBalance}
              superEthBalance={superEthBalance}
            />

            {/* Network Stats */}
            <NetworkStats />
          </div>
        </div>
      </main>
    </div>
  );
};

export default BridgePage;