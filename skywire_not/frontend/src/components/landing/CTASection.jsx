// src/components/landing/CTASection.jsx
import React from "react";
import Logo from "../common/Logo";
import { PrimaryButton, SecondaryButton } from "../common/Button";
import { ChevronRight } from "lucide-react";

const CTASection = () => {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-teal-500/20 rounded-3xl blur-3xl -z-10"></div>
          <div className="border border-white/10 rounded-3xl backdrop-blur-sm bg-white/5 p-12">
            <div className="grid md:grid-cols-2 gap-10 items-center">
              <div>
                <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Experience the Future of Cross-Chain Transfers?</h2>
                <p className="text-slate-300 mb-8">
                  Join thousands of users who trust Skywire for their cross-chain transfers. Experience the future of blockchain interoperability today.
                </p>
                <div className="flex flex-col sm:flex-row gap-4">
                  <PrimaryButton>
                    Launch App <ChevronRight size={16} />
                  </PrimaryButton>
                  <SecondaryButton>
                    View Documentation
                  </SecondaryButton>
                </div>
              </div>
              <div className="relative">
                <div className="aspect-square max-w-md mx-auto">
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="relative h-48 w-48">
                    <div className="relative h-48 w-48">
                        <div className="absolute inset-0 animate-spin-slow">
                          <div className="h-full w-full rounded-full border-2 border-dashed border-cyan-400/50"></div>
                        </div>
                        <div className="absolute inset-4 animate-spin-slow-reverse">
                          <div className="h-full w-full rounded-full border-2 border-dashed border-teal-400/50"></div>
                        </div>
                        <div className="absolute inset-8 animate-pulse">
                          <div className="h-full w-full rounded-full bg-gradient-to-r from-cyan-500/30 to-teal-500/30 flex items-center justify-center">
                            <Logo />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTASection;