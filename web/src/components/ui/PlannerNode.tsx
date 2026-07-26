import React from 'react';
import { motion } from 'framer-motion';

interface PlannerNodeProps {
  stepNumber: number;
  taskName: string;
  status: 'COMPLETED' | 'EXECUTING' | 'PENDING';
}

export const PlannerNode: React.FC<PlannerNodeProps> = ({ stepNumber, taskName, status }) => {
  const statusStyles = {
    COMPLETED: 'bg-emerald-500/20 border-emerald-500 text-emerald-400',
    EXECUTING: 'bg-amber-500/20 border-amber-500 text-amber-400 font-bold animate-pulse',
    PENDING: 'bg-slate-950 border-slate-800 text-slate-500',
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`p-3 rounded-xl border flex items-center justify-between font-mono text-xs ${statusStyles[status]}`}
    >
      <span>{stepNumber}. {taskName}</span>
      <span className="text-[10px] font-bold tracking-wider">{status}</span>
    </motion.div>
  );
};
