// src/pages/BridgePage.jsx
import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { NavLink } from 'react-router-dom';
import { ArrowLeftRight, Activity } from 'lucide-react';
import Logo from '../components/common/Logo';
import BridgeBackground from '../components/common/BridgeBackground';
import { TabButton } from '../components/common/Inputs';
import ActionSelector from '../components/bridge/ActionSelector';
import BridgeForm from '../components/Bridge/BridgeForm';
import DepositForm from '../components/bridge/DepositForm';
import WithdrawForm from '../components/bridge/WithdrawForm';
import StatusDisplay from '../components/bridge/StatusDisplay';
import BalanceDisplay from '../components/bridge/BalanceDisplay';
import NetworkStats from '../components/bridge/NetworkStats';
import WalletButton from '../components/bridge/ConnectButton';
import { SUPERETH_ABI, CONTRACT_ADDRESS, SUPPORTED_CHAINS } from '../components/constants/chain';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';

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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-indigo-900">
      <Navbar />
      
      <main className="container mx-auto px-4 py-12">
        <div className="text-center mb-12" data-aos="fade-up">
          <h1 className="text-4xl font-bold text-white mb-4">Cross-Chain Bridge</h1>
          <p className="text-gray-300 max-w-2xl mx-auto">
            Transfer your tokens across different blockchain networks securely and efficiently
            using Skywire's AI-powered bridging protocol.
          </p>
        </div>
        
        <div className="max-w-4xl mx-auto" data-aos="fade-up" data-aos-delay="200">
          <BridgeForm />
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default BridgePage;