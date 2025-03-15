// src/components/common/Inputs.jsx
import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const NetworkSelector = ({ value, onChange, options, label }) => {
  const [isOpen, setIsOpen] = useState(false);
  const selected = options.find(opt => opt.chainId === value);

  return (
    <div className="relative">
      <label className="block text-sm text-slate-400 mb-2">{label}</label>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 rounded-xl bg-slate-900/70 backdrop-blur-sm border border-white/10 
                 flex items-center justify-between text-left hover:border-cyan-500/50 
                 transition-all duration-200"
        type="button"
      >
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{selected?.icon}</span>
          <div>
            <div className="font-medium text-white">{selected?.chainName}</div>
            <div className="text-sm text-slate-400">Network</div>
          </div>
        </div>
        <ChevronDown className={`text-cyan-400 transform transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute z-50 w-full mt-2 rounded-xl bg-slate-900/90 backdrop-blur-sm 
                     border border-white/10 shadow-xl shadow-cyan-500/5 overflow-hidden"
          >
            {options.map((option) => (
              <button
                key={option.chainId}
                onClick={() => {
                  onChange(option.chainId);
                  setIsOpen(false);
                }}
                className="w-full p-4 flex items-center space-x-3 hover:bg-cyan-500/10 
                         transition-colors duration-200"
                type="button"
              >
                <span className="text-2xl">{option.icon}</span>
                <div>
                  <div className="font-medium text-white">{option.chainName}</div>
                  <div className="text-sm text-slate-400">Network</div>
                </div>
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export const AmountInput = ({ value, onChange, label, placeholder = "0.0", tokenSymbol = "ETH" }) => (
  <div className="space-y-2">
    <label className="block text-sm text-slate-400">{label}</label>
    <div className="relative">
      <input
        type="text"
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full p-4 rounded-xl bg-slate-900/70 backdrop-blur-sm border border-white/10 
                 text-white placeholder-slate-500 text-lg font-medium
                 focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 
                 transition-all duration-200"
      />
      <div className="absolute right-4 top-1/2 -translate-y-1/2 
                    px-3 py-1 rounded-lg bg-slate-800/70 text-sm font-medium text-cyan-400">
        {tokenSymbol}
      </div>
    </div>
  </div>
);

export const AddressInput = ({ value, onChange }) => (
  <div className="space-y-2">
    <label className="block text-sm text-slate-400">Recipient Address</label>
    <input
      type="text"
      value={value}
      onChange={onChange}
      placeholder="0x..."
      className="w-full p-4 rounded-xl bg-slate-900/70 backdrop-blur-sm border border-white/10 
               text-white placeholder-slate-500 font-medium
               focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 
               transition-all duration-200"
    />
  </div>
);

export const BridgeActionButton = ({ onClick, icon: Icon, label, description, active = false }) => (
  <button
    onClick={onClick}
    className={`w-full p-4 rounded-xl backdrop-blur-sm border transition-all duration-300
              ${active 
                ? 'bg-cyan-500/10 border-cyan-500/50 shadow-lg shadow-cyan-500/10' 
                : 'bg-slate-900/50 border-white/10 hover:border-cyan-500/30 hover:bg-slate-900/70'}`}
    type="button"
  >
    <div className="flex items-center space-x-4">
      <div className={`w-12 h-12 rounded-xl ${active ? 'bg-gradient-to-br from-cyan-400 to-teal-500' : 'bg-cyan-500/20'} flex items-center justify-center ${active ? 'text-black' : 'text-cyan-400'}`}>
        <Icon size={24} />
      </div>
      <div className="text-left">
        <div className="font-medium">{label}</div>
        <div className="text-sm text-slate-400">{description}</div>
      </div>
    </div>
  </button>
);

export const TabButton = ({ active, onClick, icon: Icon, label }) => (
  <button
    onClick={onClick}
    type="button"
    className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors duration-200
      ${active ? 'bg-gradient-to-r from-cyan-500/20 to-teal-500/20 text-cyan-400' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'}`}
  >
    <Icon size={18} />
    <span>{label}</span>
  </button>
);