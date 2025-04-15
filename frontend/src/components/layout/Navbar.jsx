import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-900/60 backdrop-blur-md border-b border-gray-800 fixed w-full z-10">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="text-white text-xl font-bold flex items-center">
              <span className="bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">Skywire</span>
              <span className="text-gray-300 ml-1">Protocol</span>
            </Link>
          </div>
          
          <div className="hidden md:flex space-x-8">
            <Link to="/" className="text-gray-300 hover:text-white transition-colors">
              Home
            </Link>
            <Link to="/app" className="text-white font-medium">
              App
            </Link>
            <a href="https://docs.skywire.protocol" target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white transition-colors">
              Docs
            </a>
            <a href="https://github.com/skywire/skywire" target="_blank" rel="noopener noreferrer" className="text-gray-300 hover:text-white transition-colors">
              GitHub
            </a>
          </div>
          
          <div className="md:hidden">
            <button className="text-gray-300 hover:text-white">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 