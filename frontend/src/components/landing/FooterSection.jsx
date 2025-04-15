// src/components/landing/FooterSection.jsx
import React from "react";
import { Link } from "react-router-dom";
import Logo from "../common/Logo";

const FooterSection = () => {
  return (
    <footer className="py-12 border-t border-white/10">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <Logo />
            <p className="mt-4 text-slate-400 max-w-xs">
              The most secure and efficient cross-chain bridge powered by SuperERC20 technology and intelligent AI agents.
            </p>
          </div>
          
          <div>
            <h4 className="font-bold mb-4">Product</h4>
            <ul className="space-y-2">
              <li><Link to="/features" className="text-slate-400 hover:text-cyan-400 transition-colors">Features</Link></li>
              <li><Link to="/security" className="text-slate-400 hover:text-cyan-400 transition-colors">Security</Link></li>
              <li><Link to="/roadmap" className="text-slate-400 hover:text-cyan-400 transition-colors">Roadmap</Link></li>
              <li><Link to="/partnerships" className="text-slate-400 hover:text-cyan-400 transition-colors">Partnerships</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-bold mb-4">Resources</h4>
            <ul className="space-y-2">
              <li><Link to="/docs" className="text-slate-400 hover:text-cyan-400 transition-colors">Documentation</Link></li>
              <li><Link to="/tutorials" className="text-slate-400 hover:text-cyan-400 transition-colors">Tutorials</Link></li>
              <li><Link to="/faq" className="text-slate-400 hover:text-cyan-400 transition-colors">FAQ</Link></li>
              <li><Link to="/community" className="text-slate-400 hover:text-cyan-400 transition-colors">Community</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-bold mb-4">Connect</h4>
            <ul className="space-y-2">
              <li><a href="https://twitter.com/Skywirebridge" className="text-slate-400 hover:text-cyan-400 transition-colors">Twitter</a></li>
              <li><a href="https://discord.gg/Skywirebridge" className="text-slate-400 hover:text-cyan-400 transition-colors">Discord</a></li>
              <li><a href="https://github.com/Skywirebridge" className="text-slate-400 hover:text-cyan-400 transition-colors">GitHub</a></li>
              <li><a href="mailto:hello@Skywirebridge.io" className="text-slate-400 hover:text-cyan-400 transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>
        
        <div className="mt-12 pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center">
          <div className="text-slate-400 text-sm">
            © 2025 Skywire Bridge. All rights reserved.
          </div>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link to="/privacy" className="text-slate-400 hover:text-cyan-400 transition-colors text-sm">Privacy Policy</Link>
            <Link to="/terms" className="text-slate-400 hover:text-cyan-400 transition-colors text-sm">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default FooterSection;