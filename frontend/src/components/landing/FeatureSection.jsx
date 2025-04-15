import React from "react";
import { Key, Shield, Zap } from "lucide-react";
import { FeatureCard } from "../common/Cards";

const FeatureSection = () => {
  return (
    <section className="py-20 relative">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Advanced Features</h2>
          <p className="text-slate-300">
            Our cutting-edge bridge combines SuperERC20 technology with AI agents to create the most secure and efficient cross-chain experience
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={Key}
            title="SuperERC20 Technology"
            description="Leverage OP's new SuperERC20 standard for improved interoperability, reducing gas costs and increasing transfer speed across blockchains."
          />
          <FeatureCard
            icon={Shield}
            title="AI-Powered Security"
            description="Our intelligent agents constantly monitor transactions, detecting and preventing potential security threats before they occur."
          />
          <FeatureCard
            icon={Zap}
            title="Lightning Fast Transfers"
            description="Experience near-instant transfers with our optimized bridging protocol, processing transactions in minutes rather than hours."
          />
        </div>
      </div>
    </section>
  );
};

export default FeatureSection;