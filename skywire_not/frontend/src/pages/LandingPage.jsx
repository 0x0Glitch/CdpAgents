// src/pages/LandingPage.jsx
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AOS from 'aos';
import 'aos/dist/aos.css';

// Import Common Components
import Logo from "../components/common/Logo";
import DynamicBackground from "../components/common/Background";

// Import Landing Page Sections
import HeroSection from "../components/landing/HeroSection";
import StatsSection from "../components/landing/StatsSection";
import FeatureSection from "../components/landing/FeatureSection";
import HowItWorksSection from "../components/landing/HowItWorksSection";
import TestimonialsSection from "../components/landing/TestimonialsSection";
import CTASection from "../components/landing/CTASection";
import FAQSection from "../components/landing/FAQSection";
import FooterSection from "../components/landing/FooterSection";

const LandingPage = () => {
  const [scrolled, setScrolled] = useState(false);

  // Initialize AOS animation library
  useEffect(() => {
    AOS.init({
      once: true,
      offset: 50,
      duration: 1000,
      easing: 'ease-out-cubic'
    });
  }, []);

  // Handle scroll for navbar transparency
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="relative text-white min-h-screen">
      {/* Dynamic Background */}
      <DynamicBackground />

      {/* Navbar */}
      <nav
        className={`fixed w-full z-50 transition-all duration-300 ${
          scrolled ? "bg-slate-950/80 backdrop-blur-md py-4 border-b border-white/5" : " py-6"
        }`}
      >
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            <Logo />
            
            <div className="flex items-center space-x-8">
              <Link to="/features" className="text-slate-300 hover:text-cyan-400 transition-colors">
                Features
              </Link>
              <Link to="/docs" className="text-slate-300 hover:text-cyan-400 transition-colors">
                Documentation
              </Link>
              <Link to="/app" className="hidden md:block">
                <button className="relative px-6 py-3 font-medium text-black rounded-lg overflow-hidden transition-all duration-300 bg-gradient-to-r from-cyan-400 to-teal-500 hover:scale-105 active:scale-95">
                  <span className="relative z-10 flex items-center justify-center gap-x-2">
                    Launch App
                  </span>
                </button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="relative z-0 bg-transparent">
        {/* Page Sections */}
        <HeroSection />
        <StatsSection />
        <FeatureSection />
        <HowItWorksSection />
        <TestimonialsSection />
        <CTASection />
        <FAQSection />
        <FooterSection />
      </div>
    </div>
  );
};

export default LandingPage;