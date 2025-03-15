import React from "react";

export const PrimaryButton = ({ children, className = "", ...props }) => (
  <button 
    className={`relative px-6 py-3 font-medium text-black rounded-lg overflow-hidden transition-all duration-300 
    bg-gradient-to-r from-cyan-400 to-teal-500 hover:scale-105 active:scale-95 ${className}`}
    {...props}
  >
    {/* Enhanced button background effects */}
    <div className="absolute inset-0 w-full h-full bg-black/10">
      <div className="absolute top-1 left-2 h-1 w-1 rounded-full bg-white/20"></div>
      <div className="absolute bottom-2 right-4 h-0.5 w-0.5 rounded-full bg-white/20"></div>
      <div className="absolute top-3 right-6 h-1 w-1 rounded-full bg-white/20"></div>
    </div>
    <span className="relative z-10 flex items-center justify-center gap-x-2">
      {children}
    </span>
  </button>
);

export const SecondaryButton = ({ children, className = "", ...props }) => (
  <button 
    className={`relative px-6 py-3 font-medium rounded-lg border border-white/20 
    hover:border-cyan-500/50 hover:bg-white/5 transition-all duration-300 ${className}`}
    {...props}
  >
    {/* Added subtle glow effect on hover */}
    <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-cyan-500/0 to-teal-500/0 hover:from-cyan-500/10 hover:to-teal-500/10 transition-all duration-300"></div>
    <span className="relative z-10 flex items-center justify-center gap-x-2">
      {children}
    </span>
  </button>
);