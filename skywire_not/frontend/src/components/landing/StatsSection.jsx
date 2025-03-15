import React from "react";
import { BarChart3, RefreshCw, Layers, Shield } from "lucide-react";
import { StatCard } from "../common/Cards";

const StatsSection = () => {
  return (
    <section className="py-10">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <StatCard value="$120M+" label="Total Volume Bridged" icon={BarChart3} />
          <StatCard value="5,600+" label="Active Users" icon={RefreshCw} />
          <StatCard value="4" label="Supported Chains" icon={Layers} />
          <StatCard value="100%" label="Secure Transactions" icon={Shield} />
        </div>
      </div>
    </section>
  );
};

export default StatsSection;