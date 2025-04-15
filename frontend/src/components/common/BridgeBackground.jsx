// src/components/common/BridgeBackground.jsx
import React from "react";
import { motion } from "framer-motion";

const BridgeBackground = () => {
  // Create hex nodes that represent blockchain networks
  const hexNodes = Array.from({ length: 15 }, (_, i) => ({
    id: `hex-${i}`,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 60 + 40,
    color: Math.random() > 0.5 ? "cyan" : "teal",
    duration: Math.random() * 20 + 20,
  }));

  // Create glowing orbs that enhance the cosmic feel
  const orbs = Array.from({ length: 12 }, (_, i) => ({
    id: `orb-${i}`,
    size: Math.random() * 5 + 2,
    duration: Math.random() * 20 + 15,
    delay: Math.random() * 5,
  }));

  // Create connection lines between nodes
  const connectionLines = Array.from({ length: 10 }, (_, i) => ({
    id: `connection-${i}`,
    start: Math.floor(Math.random() * hexNodes.length),
    end: Math.floor(Math.random() * hexNodes.length),
    duration: Math.random() * 8 + 7,
    delay: Math.random() * 4,
  }));

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {/* Dark background with subtle gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
      
      {/* Network nodes (hexagons) */}
      <div className="absolute inset-0 opacity-20">
        {hexNodes.map((node) => (
          <motion.div
            key={node.id}
            className={`absolute w-12 h-12 border ${node.color === 'cyan' ? 'border-cyan-500/30' : 'border-teal-500/30'}`}
            style={{
              left: `${node.x}%`,
              top: `${node.y}%`,
              width: `${node.size}px`,
              height: `${node.size}px`,
              clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
            }}
            animate={{
              opacity: [0.1, 0.3, 0.1],
              scale: [1, 1.05, 1],
              rotate: [0, 5, 0, -5, 0],
            }}
            transition={{
              duration: node.duration,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        ))}
      </div>

      {/* Connection lines (animated data transfers) */}
      <div className="absolute inset-0">
        {connectionLines.map((line) => {
          // Make sure we don't connect a node to itself
          const endIndex = line.start === line.end 
            ? (line.end + 1) % hexNodes.length 
            : line.end;
            
          const startNode = hexNodes[line.start];
          const endNode = hexNodes[endIndex];
          
          return (
            <motion.div
              key={line.id}
              className="absolute top-0 left-0 w-full h-full"
              style={{
                overflow: 'hidden',
              }}
            >
              <motion.div
                className="absolute h-[1px] bg-gradient-to-r from-cyan-500/40 to-transparent"
                style={{
                  top: `${startNode.y}%`,
                  left: `${startNode.x}%`,
                  width: '0%',
                  transformOrigin: 'left',
                }}
                animate={{
                  width: [`0%`, `${Math.sqrt(Math.pow(endNode.x - startNode.x, 2) + Math.pow(endNode.y - startNode.y, 2))}%`],
                  left: [`${startNode.x}%`, `${startNode.x}%`],
                  top: [`${startNode.y}%`, `${startNode.y}%`],
                  rotate: [
                    `${Math.atan2(endNode.y - startNode.y, endNode.x - startNode.x) * (180 / Math.PI)}deg`,
                    `${Math.atan2(endNode.y - startNode.y, endNode.x - startNode.x) * (180 / Math.PI)}deg`
                  ],
                  opacity: [0, 0.8, 0]
                }}
                transition={{
                  duration: line.duration,
                  ease: "easeInOut",
                  delay: line.delay,
                  repeat: Infinity,
                  repeatDelay: Math.random() * 5 + 5,
                }}
              />
              <motion.div
                className="absolute h-2 w-2 rounded-full bg-cyan-400"
                animate={{
                  left: [`${startNode.x}%`, `${endNode.x}%`],
                  top: [`${startNode.y}%`, `${endNode.y}%`],
                  opacity: [0, 1, 0]
                }}
                transition={{
                  duration: line.duration * 0.8,
                  ease: "easeInOut",
                  delay: line.delay + 0.2,
                  repeat: Infinity,
                  repeatDelay: Math.random() * 5 + 5,
                }}
              />
            </motion.div>
          );
        })}
      </div>

      {/* Glowing orbs */}
      {orbs.map((orb) => (
        <motion.div
          key={orb.id}
          className="absolute rounded-full"
          style={{
            width: `${orb.size}rem`,
            height: `${orb.size}rem`,
            background: 'radial-gradient(circle at 30% 30%, rgba(6, 182, 212, 0.12), rgba(20, 184, 166, 0.05))',
            boxShadow: '0 0 30px 5px rgba(6, 182, 212, 0.08)',
            opacity: 0.7,
          }}
          animate={{
            x: [
              Math.random() * window.innerWidth,
              Math.random() * window.innerWidth,
              Math.random() * window.innerWidth,
            ],
            y: [
              Math.random() * window.innerHeight,
              Math.random() * window.innerHeight,
              Math.random() * window.innerHeight,
            ],
            scale: [1, 1.2, 0.8, 1],
            opacity: [0.3, 0.7, 0.3],
          }}
          transition={{
            duration: orb.duration,
            delay: orb.delay,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      ))}

      {/* Subtle grid pattern */}
      <div 
        className="absolute inset-0 opacity-5" 
        style={{
          backgroundSize: '40px 40px',
          backgroundImage: `
            linear-gradient(to right, rgba(20, 184, 166, 0.2) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(20, 184, 166, 0.2) 1px, transparent 1px)
          `,
          backgroundPosition: 'center center',
        }}
      />
    </div>
  );
};

export default BridgeBackground;