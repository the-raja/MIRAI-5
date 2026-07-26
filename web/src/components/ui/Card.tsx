import React from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  glow?: 'blue' | 'purple' | 'emerald' | 'amber' | 'red' | 'none';
}

export const Card: React.FC<CardProps> = ({ children, className = '', glow = 'none' }) => {
  const glowStyles = {
    blue: 'shadow-blue-500/10 border-blue-500/30',
    purple: 'shadow-purple-500/10 border-purple-500/30',
    emerald: 'shadow-emerald-500/10 border-emerald-500/30',
    amber: 'shadow-amber-500/10 border-amber-500/30',
    red: 'shadow-red-500/10 border-red-500/30',
    none: 'border-slate-800',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-slate-900/80 backdrop-blur-xl border rounded-2xl p-5 shadow-2xl ${glowStyles[glow]} ${className}`}
    >
      {children}
    </motion.div>
  );
};
