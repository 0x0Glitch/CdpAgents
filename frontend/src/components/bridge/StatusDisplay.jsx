import React from 'react';
import { Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const StatusDisplay = ({ statusMessage }) => {
  if (!statusMessage) return null;
  
  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        className="p-4 rounded-xl bg-gradient-to-r from-cyan-500/10 to-teal-500/10 border border-cyan-500/20"
      >
        <div className="flex items-center space-x-3 text-cyan-400">
          <Activity size={20} className="animate-pulse" />
          <span>{statusMessage}</span>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

export default StatusDisplay;