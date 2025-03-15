// src/components/bridge/ConnectButton.jsx
import React from 'react';
import { Wallet } from 'lucide-react';
import { PrimaryButton } from '../common/Button';
import { motion } from 'framer-motion';

const ConnectButton = ({ connectWallet }) => (
  <PrimaryButton 
    onClick={connectWallet} 
    className="px-6 py-3"
  >
    <motion.span
      animate={{ scale: [1, 1.05, 1] }}
      transition={{ duration: 2, repeat: Infinity }}
      className="flex items-center space-x-2"
    >
      <Wallet size={20} />
      <span>Connect Wallet</span>
    </motion.span>
  </PrimaryButton>
);

const UserAddress = ({ address }) => (
  <div className="flex items-center space-x-2">
    <div className="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500/10 to-teal-500/10 border border-white/10">
      <div className="text-sm font-mono">
        {address.slice(0, 6)}...{address.slice(-4)}
      </div>
    </div>
  </div>
);

const WalletButton = ({ userAddress, connectWallet }) => {
  return userAddress ? <UserAddress address={userAddress} /> : <ConnectButton connectWallet={connectWallet} />;
};

export default WalletButton;