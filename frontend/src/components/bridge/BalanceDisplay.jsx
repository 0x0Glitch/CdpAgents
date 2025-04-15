// src/components/bridge/BalanceDisplay.jsx
import React from 'react';
import { FrostedCard } from '../common/Cards';

const BalanceDisplay = ({ ethBalance, superEthBalance }) => {
  return (
    <FrostedCard>
      <h3 className="text-xl font-bold mb-6">Your Balances</h3>
      <div className="space-y-4">
        <div className="p-4 rounded-xl bg-slate-900/50 border border-white/10 flex items-center space-x-4 transform transition-all duration-300 hover:border-cyan-500/30 hover:translate-y-[-2px]">
          <div className="relative w-12 h-12 flex-shrink-0">
            <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-cyan-500/20 to-teal-500/20 blur-md"></div>
            <div className="relative h-full w-full rounded-lg flex items-center justify-center font-bold text-cyan-400">
              ETH
            </div>
          </div>
          <div className="flex-1">
            <div className="text-sm text-slate-400">Available ETH</div>
            <div className="font-bold text-white text-lg">{ethBalance} ETH</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/50 border border-white/10 flex items-center space-x-4 transform transition-all duration-300 hover:border-teal-500/30 hover:translate-y-[-2px]">
          <div className="relative w-12 h-12 flex-shrink-0">
            <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-teal-500/20 to-cyan-500/20 blur-md"></div>
            <div className="relative h-full w-full rounded-lg flex items-center justify-center font-bold text-teal-400">
              sETH
            </div>
          </div>
          <div className="flex-1">
            <div className="text-sm text-slate-400">SuperETH Balance</div>
            <div className="font-bold text-white text-lg">{superEthBalance} sETH</div>
          </div>
        </div>
      </div>
    </FrostedCard>
  );
};

export default BalanceDisplay;