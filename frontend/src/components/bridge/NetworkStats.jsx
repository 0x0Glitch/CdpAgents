// src/components/bridge/NetworkStats.jsx
import React from 'react';
import { ShieldCheck, Rocket, Layers, BarChart3 } from 'lucide-react';
import { FrostedCard } from '../common/Cards';

const StatItem = ({ label, value, icon: Icon, subtext = null }) => (
  <div className="p-4 rounded-xl bg-slate-900/50 border border-white/10 transition-all duration-300 hover:border-cyan-500/30 hover:bg-slate-900/70">
    <div className="flex items-center justify-between">
      <div className="space-y-1">
        <p className="text-sm text-slate-400">{label}</p>
        <p className="font-medium text-white">{value}</p>
        {subtext && <p className="text-xs text-slate-500">{subtext}</p>}
      </div>
      {Icon && (
        <div className="relative w-10 h-10">
          <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-cyan-500/10 to-teal-500/10 blur-md"></div>
          <div className="relative h-full w-full rounded-lg flex items-center justify-center">
            <Icon className="text-cyan-400" size={18} />
          </div>
        </div>
      )}
    </div>
  </div>
);

const NetworkStats = () => {
  return (
    <FrostedCard>
      <h3 className="text-xl font-bold mb-6">Protocol Stats</h3>
      <div className="grid gap-4">
        <StatItem
          label="Total Value Locked"
          value="$42.8M"
          icon={BarChart3}
          subtext="Across all chains"
        />
        <StatItem
          label="Average Bridge Time"
          value="73 seconds"
          icon={Rocket}
          subtext="SuperERC20 optimized"
        />
        <StatItem
          label="Supported Networks"
          value="4 chains"
          icon={Layers}
          subtext="Ethereum, Optimism, Base, Zora"
        />
        <div className="p-4 rounded-xl bg-slate-900/50 border border-white/10">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <ShieldCheck size={16} className="text-green-400" />
              <span className="text-sm text-slate-400">Security Status</span>
            </div>
            <span className="font-medium text-green-400">Secured</span>
          </div>
          <div className="h-2 rounded-full bg-slate-800">
            <div 
              className="h-full rounded-full bg-gradient-to-r from-green-500 to-cyan-500"
              style={{ width: '98%' }}
            />
          </div>
          <div className="mt-2 text-xs text-slate-500 text-right">
            Audited by ChainSec
          </div>
        </div>
      </div>
    </FrostedCard>
  );
};

export default NetworkStats;