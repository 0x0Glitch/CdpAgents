import React from "react";
import { Check } from "lucide-react";

export const CosmicCard = ({ children, className = "", hoverable = true, glow = "cyan" }) => {
  const glowColors = {
    cyan: "from-cyan-500/15 to-teal-500/15",
    teal: "from-teal-500/15 to-cyan-500/15",
    blue: "from-blue-500/15 to-cyan-500/15",
    purple: "from-purple-500/15 to-cyan-500/15",
    green: "from-green-500/15 to-teal-500/15"
  };

  const selectedGlow = glowColors[glow] || glowColors.cyan;

  return (
    <div className={`relative group ${className}`}>
      {/* Enhanced glow effect */}
      <div className={`absolute -inset-0.5 rounded-2xl bg-gradient-to-r ${selectedGlow} opacity-0 blur-lg transition-all duration-500 ease-in-out group-hover:opacity-100`} />
      
      {/* Animated border gradient */}
      <div className="absolute inset-0 rounded-2xl p-[1px] bg-gradient-to-r from-cyan-500/20 via-slate-800/5 to-teal-500/20 overflow-hidden">
        {/* Card content */}
        <div 
          className={`h-full w-full flex flex-col rounded-2xl border-0 bg-slate-900/80 backdrop-blur-md p-6 overflow-hidden ${
            hoverable ? "transition-all duration-300 ease-in-out group-hover:translate-y-[-2px] group-hover:shadow-lg group-hover:shadow-cyan-500/5" : ""
          }`}
        >
          {/* Decorative element - subtle network nodes in background */}
          <div className="absolute top-0 right-0 w-32 h-32 opacity-5">
            <div className="absolute top-6 right-10 h-1 w-1 rounded-full bg-cyan-400"></div>
            <div className="absolute top-12 right-20 h-1.5 w-1.5 rounded-full bg-teal-400"></div>
            <div className="absolute top-24 right-8 h-1 w-1 rounded-full bg-cyan-400"></div>
            <div className="absolute top-16 right-14 h-0.5 w-0.5 rounded-full bg-white"></div>
            <div className="absolute top-20 right-28 h-1 w-1 rounded-full bg-teal-400"></div>
            {/* Subtle connection lines */}
            <div className="absolute top-6 right-10 w-10 h-[1px] bg-cyan-400/20 rotate-[30deg]"></div>
            <div className="absolute top-12 right-20 w-12 h-[1px] bg-teal-400/20 rotate-[-20deg]"></div>
            <div className="absolute top-20 right-14 w-14 h-[1px] bg-cyan-400/20 rotate-[70deg]"></div>
          </div>
          
          {/* Actual content */}
          <div className="relative z-10">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export const FeatureCard = ({ icon: Icon, title, description }) => (
 <FrostedCard >
    <div className="flex flex-col h-full">
      <div className="mb-6 relative w-16 h-16">
        {/* Enhanced icon container with animated glow */}
        <div className="absolute -inset-1 rounded-xl bg-gradient-to-br from-cyan-400/40 to-teal-600/40 blur-md opacity-75 group-hover:opacity-100 transition-opacity duration-500"></div>
        <div className="relative w-full h-full rounded-xl bg-gradient-to-br from-cyan-400 to-teal-600 flex items-center justify-center overflow-hidden">
          {/* Decorative background pattern */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-1 left-1 h-1 w-1 rounded-full bg-white"></div>
            <div className="absolute bottom-2 right-2 h-1 w-1 rounded-full bg-white"></div>
            <div className="absolute top-3 right-3 h-0.5 w-0.5 rounded-full bg-white"></div>
          </div>
          <Icon size={24} className="text-black relative z-10" />
        </div>
      </div>
      <h3 className="text-xl font-bold text-white mb-3">{title}</h3>
      <p className="text-slate-300 mt-1">{description}</p>
    </div>
    </FrostedCard>

);

export const StepCard = ({ number, title, description, glow = "cyan" }) => (
  <FrostedCard glow={glow}>
    <div className="flex flex-col items-start">
      <div className="flex items-center space-x-4 mb-4">
        <div className="relative">
          {/* Enhanced step number with pulsing animation */}
          <div className="absolute -inset-1 rounded-full bg-gradient-to-r from-cyan-500/40 to-teal-500/40 blur-md animate-pulse-slow"></div>
          <div className="relative h-10 w-10 rounded-full bg-gradient-to-r from-cyan-500 to-teal-500 flex items-center justify-center text-black font-bold">
            {number}
          </div>
        </div>
        <h3 className="text-xl font-bold text-white">{title}</h3>
      </div>
      <p className="text-slate-300">{description}</p>
    </div>
  </FrostedCard>
);
export const FrostedCard = ({ children, className = "", hoverable = true }) => (
    <div className={`relative group ${className}`}>
      <div className="absolute -inset-0.5 rounded-2xl bg-gradient-to-r from-cyan-500/10 to-teal-500/10 opacity-3 blur-lg transition-all duration-300 group-hover:opacity-100" />
      <div 
        className={`h-full flex flex-col rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm p-6 overflow-hidden ${
          hoverable ? "transition-all duration-300 group-hover:translate-y-[-2px] group-hover:shadow-lg" : ""
        }`}
      >
        {children}
      </div>
    </div>
  );

export const StatCard = ({ value, label, icon: Icon }) => (
  <FrostedCard hoverable={false}>
    <div className="flex items-center justify-between">
      <div>
        <div className="text-3xl font-bold text-white mb-1 group-hover:text-cyan-400 transition-colors duration-300">{value}</div>
        <div className="text-slate-400 text-sm">{label}</div>
      </div>
      <div className="relative h-12 w-12">
        {/* Enhanced icon container with animated glow */}
        <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-cyan-400/20 to-teal-600/20 blur-md group-hover:from-cyan-400/40 group-hover:to-teal-600/40 transition-all duration-300"></div>
        <div className="relative h-full w-full rounded-xl flex items-center justify-center">
          <Icon size={24} className="text-cyan-400" />
        </div>
      </div>
    </div>
  </FrostedCard>
);