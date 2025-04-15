import React from "react";
import { FrostedCard } from "../common/Cards";

const TestimonialsSection = () => {
  return (
    <section className="py-20 relative">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">What Users Say</h2>
          <p className="text-slate-300">
            Join thousands of satisfied users who trust our bridge for their cross-chain transfers
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          <FrostedCard>
            <div className="flex flex-col h-full">
              <div className="flex-1">
                <p className="text-slate-300">
                  "Skywire has completely transformed how I move assets between blockchains. The AI-powered security gives me confidence that my funds are safe."
                </p>
              </div>
              <div className="mt-6 pt-6 border-t border-white/10">
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-cyan-500/20 flex items-center justify-center text-cyan-400 font-bold">
                    JD
                  </div>
                  <div className="ml-4">
                    <div className="font-medium">John Doe</div>
                    <div className="text-sm text-slate-400">DeFi Developer</div>
                  </div>
                </div>
              </div>
            </div>
          </FrostedCard>
          
          <FrostedCard>
            <div className="flex flex-col h-full">
              <div className="flex-1">
                <p className="text-slate-300">
                  "The speed of transfers is incredible. What used to take hours now completes in minutes, and the gasless transactions save me a fortune."
                </p>
              </div>
              <div className="mt-6 pt-6 border-t border-white/10">
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-teal-500/20 flex items-center justify-center text-teal-400 font-bold">
                    AS
                  </div>
                  <div className="ml-4">
                    <div className="font-medium">Alice Smith</div>
                    <div className="text-sm text-slate-400">Crypto Trader</div>
                  </div>
                </div>
              </div>
            </div>
          </FrostedCard>
          
          <FrostedCard>
            <div className="flex flex-col h-full">
              <div className="flex-1">
                <p className="text-slate-300">
                  "As someone who works across multiple blockchains, Skywire Bridge has become an essential tool in my daily workflow. The UI is intuitive and the service is reliable."
                </p>
              </div>
              <div className="mt-6 pt-6 border-t border-white/10">
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-bold">
                    RJ
                  </div>
                  <div className="ml-4">
                    <div className="font-medium">Robert Johnson</div>
                    <div className="text-sm text-slate-400">NFT Artist</div>
                  </div>
                </div>
              </div>
            </div>
          </FrostedCard>
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;