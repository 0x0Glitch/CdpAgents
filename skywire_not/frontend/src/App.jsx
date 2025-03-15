// src/App.jsx
import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AOS from 'aos';
import 'aos/dist/aos.css';
import LandingPage from './pages/LandingPage';
import BridgePage from './pages/BridgePage';
import './index.css';

// Add custom animations to CSS
const CustomStyles = () => (
  <style>{`
    @keyframes spin-slow {
      from {
        transform: rotate(0deg);
      }
      to {
        transform: rotate(360deg);
      }
    }
    
    @keyframes spin-slow-reverse {
      from {
        transform: rotate(0deg);
      }
      to {
        transform: rotate(-360deg);
      }
    }
    
    .animate-spin-slow {
      animation: spin-slow 8s linear infinite;
    }
    
    .animate-spin-slow-reverse {
      animation: spin-slow-reverse 8s linear infinite;
    }

    .animate-pulse-slow {
      animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    @keyframes pulse {
      0%, 100% {
        opacity: 0.5;
      }
      50% {
        opacity: 1;
      }
    }

    @keyframes pulse-glow {
      0%, 100% {
        opacity: 0.6;
        transform: scale(1);
      }
      50% {
        opacity: 1;
        transform: scale(1.05);
      }
    }

    .animate-pulse-glow {
      animation: pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    @keyframes float {
      0%, 100% {
        transform: translateY(0);
      }
      50% {
        transform: translateY(-10px);
      }
    }

    .animate-float {
      animation: float 5s ease-in-out infinite;
    }

    /* Gradient text */
    .text-gradient {
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  `}</style>
);

function App() {
  useEffect(() => {
    AOS.init({
      once: true,
      offset: 50,
      duration: 1000,
      easing: 'ease-out-cubic'
    });
  }, []);

  return (
    <Router>
      <CustomStyles />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app" element={<BridgePage />} />
        <Route path="*" element={<LandingPage />} />
      </Routes>
    </Router>
  );
}

export default App;