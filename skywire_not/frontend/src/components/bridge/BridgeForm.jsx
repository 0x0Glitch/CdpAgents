// src/components/bridge/BridgeForm.jsx
import React from 'react';
import { ChevronRight } from 'lucide-react';
import { NetworkSelector, AmountInput, AddressInput } from '../common/Inputs';
import { PrimaryButton } from '../common/Button';
import { FrostedCard } from '../common/Cards';

const BridgeForm = ({ 
  bridgeAmount, 
  setBridgeAmount,
  bridgeSourceChain,
  setBridgeSourceChain,
  bridgeTargetChain,
  setBridgeTargetChain,
  bridgeRecipient,
  setBridgeRecipient,
  handleBridge,
  supportedChains,
  disabled
}) => {
  return (
    <FrostedCard glow="cyan">
      <div className="space-y-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Bridge ETH</h2>
          <div className="h-8 w-8 rounded-full bg-gradient-to-r from-cyan-500/20 to-teal-500/20 flex items-center justify-center">
            <ChevronRight className="text-cyan-400" size={16} />
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <NetworkSelector
            label="Source Network"
            value={bridgeSourceChain.chainId}
            options={supportedChains}
            onChange={(chainId) => {
              const chainData = supportedChains.find(c => c.chainId === chainId);
              if (chainData) setBridgeSourceChain(chainData);
            }}
          />
          <NetworkSelector
            label="Destination Network"
            value={bridgeTargetChain.chainId}
            options={supportedChains}
            onChange={(chainId) => {
              const chainData = supportedChains.find(c => c.chainId === chainId);
              if (chainData) setBridgeTargetChain(chainData);
            }}
          />
        </div>

        <AmountInput
          label="Amount to Bridge"
          value={bridgeAmount}
          onChange={(e) => setBridgeAmount(e.target.value)}
          tokenSymbol="ETH"
        />

        <AddressInput
          value={bridgeRecipient}
          onChange={(e) => setBridgeRecipient(e.target.value)}
        />

        <div className="pt-4">
          <PrimaryButton
            onClick={handleBridge}
            disabled={disabled}
            className="w-full py-4"
          >
            <span>Bridge Your ETH</span>
            <ChevronRight size={20} />
          </PrimaryButton>
        </div>
      </div>
    </FrostedCard>
  );
};

export default BridgeForm;