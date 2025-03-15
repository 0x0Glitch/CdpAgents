import React from "react";
import { Link } from "react-router-dom";
import { ArrowRightLeft, Check } from "lucide-react";
import { PrimaryButton, SecondaryButton } from "../common/Button";

const HeroSection = () => {
  return (
    <section className="pt-20 pb-16 md:pt-36 md:pb-20 relative">
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-10 items-center">
          <div className="">
            <div className="inline-block px-3 py-1 rounded-full bg-white/5 border border-white/10 text-cyan-400 font-medium text-sm mb-6">
              Powered by SuperERC20s
            </div>
            <h1 className="text-5xl md:text-6xl font-bold leading-tight">
              <span className="inline-block">Seamless</span>{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-teal-500">
                Cross-Chain
              </span>{" "}
              <span className="inline-block">Transfers</span>
            </h1>
            <p className="text-xl text-slate-300 mt-6 mb-8 max-w-lg">
              Bridge tokens effortlessly across blockchains with our powerful SuperERC20 technology, backed by Skywire AI agents for increased security and speed.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <PrimaryButton>
                Connect Wallet
              </PrimaryButton>
              <SecondaryButton>
                Explore Features
              </SecondaryButton>
            </div>
            
            <div className="mt-12 flex flex-wrap gap-6">
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-green-500/10 flex items-center justify-center">
                  <Check size={16} className="text-green-500" />
                </div>
                <span className="text-slate-300">Gasless Transfers</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-green-500/10 flex items-center justify-center">
                  <Check size={16} className="text-green-500" />
                </div>
                <span className="text-slate-300">100% Secure</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-full bg-green-500/10 flex items-center justify-center">
                  <Check size={16} className="text-green-500" />
                </div>
                <span className="text-slate-300">Multi-Chain Support</span>
              </div>
            </div>
          </div>
          
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-teal-500/20 rounded-3xl blur-3xl -z-10"></div>
            <div className="border border-white/10 rounded-3xl backdrop-blur-sm bg-white/5 p-6 md:p-8">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-bold text-xl">Quick Bridge</h3>
                <div className="h-8 w-8 rounded-full bg-white/5 flex items-center justify-center">
                  <ArrowRightLeft size={16} className="text-slate-300" />
                </div>
              </div>
              
              <div className="space-y-6">
                <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-slate-400 text-sm">From</span>
                    <div className="flex items-center gap-2">
                      <div className="h-5 w-5 rounded-full bg-blue-500"></div>
                      <span className="font-medium">Ethereum</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <input
                      type="text"
                      value="1.0"
                      className="bg-transparent text-xl font-bold focus:outline-none w-full"
                      readOnly
                    />
                    <span className="text-lg font-medium">ETH</span>
                  </div>
                </div>
                
                <div className="flex justify-center">
                <div className="h-10 w-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center">
                    <ArrowRightLeft size={20} className="text-cyan-400" />
                  </div>
                </div>
                
                <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-slate-400 text-sm">To</span>
                    <div className="flex items-center gap-2">
                      <div className="h-5 w-5 rounded-full bg-green-500"></div>
                      <span className="font-medium">Optimism</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <input
                      type="text"
                      value="1.0"
                      className="bg-transparent text-xl font-bold focus:outline-none w-full"
                      readOnly
                    />
                    <span className="text-lg font-medium">sETH</span>
                  </div>
                </div>
                
                <div className="p-4 rounded-xl bg-white/5 border border-white/10">
                  <div className="flex justify-between items-center text-sm text-slate-400">
                    <span>Estimated Time</span>
                    <span>1-2 minutes</span>
                  </div>
                  <div className="flex justify-between items-center text-sm text-slate-400 mt-2">
                    <span>Bridge Fee</span>
                    <span>0.002 ETH</span>
                  </div>
                </div>
                <Link to="/app" className="hidden md:block">
                <PrimaryButton className="w-full py-4">
                  Bridge Tokens
                </PrimaryButton>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;