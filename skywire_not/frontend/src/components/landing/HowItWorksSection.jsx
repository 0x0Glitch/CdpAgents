// src/components/landing/HowItWorksSection.jsx
import React, { useEffect } from "react";
import { Check, ChevronRight, PanelRight } from "lucide-react";
import { StepCard } from "../common/Cards";
import { PrimaryButton } from "../common/Button";
import { Link } from "react-router-dom";

const HowItWorksSection = () => {
  // Initialize AOS if it's imported elsewhere
  useEffect(() => {
    if (typeof AOS !== 'undefined') {
      AOS.refresh();
    }
  }, []);

  return (
    <section className="py-28 relative overflow-hidden">
      {/* Background cosmic elements */}
      <div className="container mx-auto px-4 relative z-10">
        {/* Section Header with enhanced styling */}
        <div className="text-center max-w-2xl mx-auto mb-20" 
            data-aos="fade-up" 
            data-aos-duration="1000">
          <div className="inline-block px-4 py-1 text-sm font-medium text-cyan-400 rounded-full bg-white/5 border border-white/10 mb-3">
            Bridge Process
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-5">
            How Skywire Works
          </h2>
          <p className="text-slate-300 text-lg">
            Our intuitive bridging process makes cross-chain token transfers simple, secure, and lightning-fast
          </p>
        </div>

        {/* Horizontal Steps Layout with AOS animations */}
        <div className="max-w-6xl mx-auto">
          {/* Step 1 */}
          <div className="mb-24 relative" data-aos="fade-right" data-aos-duration="1000">
            {/* Step number indicator for larger screens */}
            <div className="hidden lg:flex absolute -left-24 top-1/2 -translate-y-1/2 items-center justify-center">
              <div className="relative h-20 w-20">
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-cyan-500/30 to-teal-500/30 blur-xl"></div>
                <div className="relative h-full w-full rounded-full border border-white/10 flex items-center justify-center">
                  <span className="text-5xl font-bold text-white">1</span>
                </div>
              </div>
            </div>
            
            {/* Connecting line to next step */}
            <div className="hidden lg:block absolute z-0 h-20 w-px bg-gradient-to-b from-cyan-500/50 to-teal-500/50 left-1/2 -bottom-20 transform -translate-x-1/2"></div>
            
            <div className="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
              {/* Left content - Connect & Deposit */}
              <div className="order-2 lg:order-1">
                <StepCard
                  number="1"
                  title="Connect & Deposit"
                  description="Connect your wallet and deposit ETH to receive SuperETH tokens at a 1:1 ratio through our secure smart contract system."
                />
                
                {/* Additional features below the step card */}
                <div className="mt-6 space-y-4 pl-14">
                  <div className="flex items-center gap-3 transform transition-all duration-300 hover:translate-x-1">
                    <div className="h-8 w-8 rounded-full bg-green-500/20 flex items-center justify-center">
                      <Check size={16} className="text-green-500" />
                    </div>
                    <span className="text-slate-300">Instant 1:1 token conversion</span>
                  </div>
                  <div className="flex items-center gap-3 transform transition-all duration-300 hover:translate-x-1">
                    <div className="h-8 w-8 rounded-full bg-green-500/20 flex items-center justify-center">
                      <Check size={16} className="text-green-500" />
                    </div>
                    <span className="text-slate-300">Zero gas fees on destination chain</span>
                  </div>
                </div>
              </div>
              
              {/* Right content - Code display */}
              <div className="order-1 lg:order-2">
                <div className="transform transition-all duration-500 hover:scale-[1.02] relative group">
                  <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-cyan-500/20 to-teal-500/20 opacity-0 blur-lg group-hover:opacity-100 transition-opacity duration-700"></div>
                  <div className="relative rounded-xl overflow-hidden border border-white/10">
                    <div className="bg-white/5 p-4 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="h-3 w-3 rounded-full bg-red-400"></div>
                        <div className="h-3 w-3 rounded-full bg-yellow-400"></div>
                        <div className="h-3 w-3 rounded-full bg-green-400"></div>
                      </div>
                      <div className="text-xs text-slate-400">Smart Contract</div>
                    </div>
                    <div className="p-6 bg-slate-900/50 backdrop-blur-sm">
                      <pre className="text-xs sm:text-sm font-mono text-slate-300 overflow-x-auto">
<code><span className="text-purple-400">function</span> <span className="text-cyan-400">deposit</span>() <span className="text-purple-400">external</span> <span className="text-purple-400">payable</span> {'{'}
  <span className="text-purple-400">require</span>(msg.value {'>'} <span className="text-orange-400">0</span>, <span className="text-green-400">"Must send ETH"</span>);
  
  <span className="text-slate-500">// Mint SuperETH tokens 1:1</span>
  <span className="text-purple-400">uint256</span> amount = msg.value;
  superETH.<span className="text-cyan-400">mint</span>(msg.sender, amount);
  
  <span className="text-purple-400">emit</span> <span className="text-cyan-400">Deposit</span>(msg.sender, amount);
{'}'}</code>
                      </pre>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Step 2 */}
          <div className="mb-24 relative" data-aos="fade-left" data-aos-duration="1000" data-aos-delay="200">
            {/* Step number indicator for larger screens */}
            <div className="hidden lg:flex absolute -right-24 top-1/2 -translate-y-1/2 items-center justify-center">
              <div className="relative h-20 w-20">
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-teal-500/30 to-cyan-500/30 blur-xl"></div>
                <div className="relative h-full w-full rounded-full border border-white/10 flex items-center justify-center">
                  <span className="text-5xl font-bold text-white">2</span>
                </div>
              </div>
            </div>
            
            {/* Connecting line to next step */}
            <div className="hidden lg:block absolute z-0 h-20 w-px bg-gradient-to-b from-teal-500/50 to-cyan-500/50 left-1/2 -bottom-20 transform -translate-x-1/2"></div>
            
            <div className="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
              {/* Left content - AI Visualization (reversed order on desktop) */}
              <div className="order-1">
                <div className="transform transition-all duration-500 hover:scale-[1.02] relative group">
                  <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-teal-500/20 to-cyan-500/20 opacity-0 blur-lg group-hover:opacity-100 transition-opacity duration-700"></div>
                  <div className="relative rounded-xl overflow-hidden border border-white/10 bg-slate-900/50 backdrop-blur-sm">
                    <div className="relative h-[280px] overflow-hidden">
                      {/* AI Processing Visualization */}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center space-y-4 px-6">
                          <div className="flex justify-center relative mb-6">
                            <div className="relative h-16 w-16 rounded-full bg-gradient-to-r from-cyan-500/20 to-teal-500/20 border border-cyan-500/40 flex items-center justify-center">
                              <div className="absolute inset-2 rounded-full border-2 border-cyan-400/30 border-dashed animate-spin-slow"></div>
                              <PanelRight size={28} className="text-cyan-400" />
                            </div>
                          </div>
                          
                          <h4 className="text-xl font-bold mb-2">AI Agent Processing</h4>
                          <p className="text-sm text-slate-400 max-w-xs mx-auto">
                            Our AI agents monitor, validate and process your transfer request in real-time
                          </p>
                        </div>
                      </div>
                      
                      {/* Animated elements */}
                      <div className="absolute top-1/4 left-1/4 h-2 w-2 rounded-full bg-cyan-500 animate-ping"></div>
                      <div className="absolute bottom-1/3 right-1/3 h-2 w-2 rounded-full bg-teal-500 animate-ping" style={{ animationDelay: "1s" }}></div>
                      <div className="absolute top-1/2 right-1/4 h-2 w-2 rounded-full bg-cyan-400 animate-ping" style={{ animationDelay: "0.5s" }}></div>
                      
                      {/* Network connection paths */}
                      <div className="absolute top-[30%] left-[30%] w-[40%] h-[1px] bg-gradient-to-r from-cyan-500/50 to-transparent"></div>
                      <div className="absolute top-[50%] right-[30%] w-[40%] h-[1px] bg-gradient-to-l from-teal-500/50 to-transparent"></div>
                      <div className="absolute bottom-[30%] left-[40%] w-[30%] h-[1px] bg-gradient-to-r from-cyan-500/50 to-transparent"></div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Right content - Choose Destination */}
              <div className="order-2">
                <StepCard
                  number="2"
                  title="Select Destination"
                  description="Choose your target blockchain network from our supported chains including Optimism, Base, Zora, and more."
                  glow="teal"
                />
                
                {/* Chain selection options */}
                <div className="mt-6 space-y-3 pl-14">
                  <div className="flex items-center gap-3 py-2 px-4 rounded-lg bg-white/5 border border-white/10 transition-all duration-300 hover:border-cyan-500/30 hover:bg-white/10 transform hover:-translate-y-1">
                    <div className="h-6 w-6 rounded-full bg-blue-500 flex-shrink-0"></div>
                    <span>Ethereum</span>
                  </div>
                  <div className="flex items-center gap-3 py-2 px-4 rounded-lg bg-gradient-to-r from-teal-500/10 to-cyan-500/10 border border-teal-500/30 transition-all duration-300 hover:from-teal-500/20 hover:to-cyan-500/20 transform hover:-translate-y-1">
                    <div className="h-6 w-6 rounded-full bg-green-500 flex-shrink-0"></div>
                    <span>Optimism</span>
                    <div className="ml-auto px-2 py-0.5 text-xs rounded-full bg-green-500/20 text-green-400">Selected</div>
                  </div>
                  <div className="flex items-center gap-3 py-2 px-4 rounded-lg bg-white/5 border border-white/10 transition-all duration-300 hover:border-cyan-500/30 hover:bg-white/10 transform hover:-translate-y-1">
                    <div className="h-6 w-6 rounded-full bg-blue-700 flex-shrink-0"></div>
                    <span>Base</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Step 3 */}
          <div className="relative" data-aos="fade-right" data-aos-duration="1000" data-aos-delay="400">
            {/* Step number indicator for larger screens */}
            <div className="hidden lg:flex absolute -left-24 top-1/2 -translate-y-1/2 items-center justify-center">
              <div className="relative h-20 w-20">
                <div className="absolute inset-0 rounded-full bg-gradient-to-r from-green-500/30 to-teal-500/30 blur-xl"></div>
                <div className="relative h-full w-full rounded-full border border-white/10 flex items-center justify-center">
                  <span className="text-5xl font-bold text-white">3</span>
                </div>
              </div>
            </div>
            
            <div className="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
              {/* Left content */}
              <div className="order-2 lg:order-1">
                <StepCard
                  number="3"
                  title="Receive Native Tokens"
                  description="Our AI agent processes your transfer and delivers native ETH to your wallet on the destination chain, completing the bridge process."
                  glow="green"
                />
                
                {/* Feature highlight */}
                <div className="mt-6 pl-14">
                  <div className="flex items-center gap-3 transform transition-all duration-300 hover:translate-x-1">
                    <div className="relative">
                      <div className="absolute inset-0 bg-green-500/20 rounded-full blur-md"></div>
                      <div className="relative h-8 w-8 rounded-full bg-green-500/20 flex items-center justify-center">
                        <Check size={16} className="text-green-500" />
                      </div>
                    </div>
                    <div>
                      <span className="text-green-500 font-medium">Ultra-fast transaction time</span>
                      <div className="text-sm text-slate-400">Complete in seconds, not hours</div>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Right content - Transaction Confirmation UI */}
              <div className="order-1 lg:order-2">
                <div className="transform transition-all duration-500 hover:scale-[1.02] relative group">
                  <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-green-500/20 to-teal-500/20 opacity-0 blur-lg group-hover:opacity-100 transition-opacity duration-700"></div>
                  <div className="relative rounded-xl overflow-hidden border border-white/10 backdrop-blur-sm bg-white/5 p-6">
                    <div className="flex items-center justify-between mb-6">
                      <div className="flex items-center gap-3">
                        <div className="relative">
                          <div className="absolute inset-0 bg-green-500/30 rounded-full blur-md"></div>
                          <div className="relative h-10 w-10 rounded-full bg-green-500/20 flex items-center justify-center">
                            <Check size={20} className="text-green-500" />
                          </div>
                        </div>
                        <div>
                          <div className="font-bold">Transfer Complete</div>
                          <div className="text-sm text-slate-400">Transaction ID: 0x71e...3f8a</div>
                        </div>
                      </div>
                      <span className="text-xs bg-green-500/20 text-green-500 px-2 py-1 rounded-full">Success</span>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="flex justify-between text-sm p-2 rounded-lg bg-white/5">
                        <span className="text-slate-400">From</span>
                        <div className="flex items-center gap-2">
                          <div className="h-4 w-4 rounded-full bg-blue-500"></div>
                          <span>Ethereum</span>
                        </div>
                      </div>
                      <div className="flex justify-between text-sm p-2 rounded-lg bg-white/5">
                        <span className="text-slate-400">To</span>
                        <div className="flex items-center gap-2">
                          <div className="h-4 w-4 rounded-full bg-green-500"></div>
                          <span>Optimism</span>
                        </div>
                      </div>
                      <div className="flex justify-between text-sm p-2 rounded-lg bg-white/5">
                        <span className="text-slate-400">Amount</span>
                        <span>1.0 ETH</span>
                      </div>
                      <div className="flex justify-between text-sm p-2 rounded-lg bg-white/5">
                        <span className="text-slate-400">Time</span>
                        <span className="text-green-400">73 seconds</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Start bridging CTA */}
        <div className="mt-20 text-center" data-aos="fade-up" data-aos-duration="1000" data-aos-delay="600">
        <Link to="/app" className="hidden md:block">
          <PrimaryButton className="px-8 py-4 text-lg">
            Start Bridging Now <ChevronRight size={18} />
          </PrimaryButton>
          </Link>
        </div>
      </div>
    </section>
  );
};
export default HowItWorksSection;