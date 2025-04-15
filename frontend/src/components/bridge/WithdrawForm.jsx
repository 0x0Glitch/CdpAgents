// src/components/bridge/WithdrawForm.jsx
import React from 'react';
import { Upload } from 'lucide-react';
import { AmountInput } from '../common/Inputs';
import { PrimaryButton } from '../common/Button';
import { FrostedCard } from '../common/Cards';

const WithdrawForm = ({ 
  withdrawAmount, 
  setWithdrawAmount, 
  handleWithdraw, 
  disabled 
}) => {
  return (
    <FrostedCard glow="green">
      <div className="space-y-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Withdraw ETH</h2>
          <div className="h-8 w-8 rounded-full bg-gradient-to-r from-green-500/20 to-teal-500/20 flex items-center justify-center">
            <Upload className="text-green-400" size={16} />
          </div>
        </div>
        
        <AmountInput
          label="Amount to Withdraw"
          value={withdrawAmount}
          onChange={(e) => setWithdrawAmount(e.target.value)}
          tokenSymbol="sETH"
        />

        <div className="rounded-xl bg-green-500/10 border border-green-500/20 p-4">
          <p className="text-sm text-slate-300">
            Convert your SuperETH tokens back to native ETH. You'll receive ETH at a 1:1 ratio minus any applicable network fees.
          </p>
        </div>

        <div className="pt-4">
          <PrimaryButton
            onClick={handleWithdraw}
            disabled={disabled}
            className="w-full py-4"
          >
            <span>Withdraw ETH</span>
            <Upload size={20} />
          </PrimaryButton>
        </div>
      </div>
    </FrostedCard>
  );
};

export default WithdrawForm;