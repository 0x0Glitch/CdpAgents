// src/components/bridge/DepositForm.jsx
import React from 'react';
import { Download } from 'lucide-react';
import { AmountInput } from '../common/Inputs';
import { PrimaryButton } from '../common/Button';
import { FrostedCard } from '../common/Cards';

const DepositForm = ({ 
  depositAmount, 
  setDepositAmount, 
  handleDeposit, 
  disabled 
}) => {
  return (
    <FrostedCard glow="teal">
      <div className="space-y-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Deposit ETH</h2>
          <div className="h-8 w-8 rounded-full bg-gradient-to-r from-teal-500/20 to-cyan-500/20 flex items-center justify-center">
            <Download className="text-teal-400" size={16} />
          </div>
        </div>
        
        <AmountInput
          label="Amount to Deposit"
          value={depositAmount}
          onChange={(e) => setDepositAmount(e.target.value)}
          tokenSymbol="ETH"
        />

        <div className="rounded-xl bg-teal-500/10 border border-teal-500/20 p-4">
          <p className="text-sm text-slate-300">
            Deposit ETH to receive SuperETH tokens at a 1:1 ratio. SuperETH tokens can be used across multiple chains and bridged instantly.
          </p>
        </div>

        <div className="pt-4">
          <PrimaryButton
            onClick={handleDeposit}
            disabled={disabled}
            className="w-full py-4"
          >
            <span>Deposit ETH</span>
            <Download size={20} />
          </PrimaryButton>
        </div>
      </div>
    </FrostedCard>
  );
};

export default DepositForm;