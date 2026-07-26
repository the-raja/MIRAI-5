import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface ButtonProps extends HTMLMotionProps<'button'> {
  variant?: 'primary' | 'secondary' | 'danger' | 'warning' | 'purple';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  children,
  className = '',
  ...props
}) => {
  const baseStyle = 'px-6 py-3 rounded-xl font-bold text-sm transition-all duration-200 shadow-lg';
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-500 text-white shadow-blue-500/20 border border-blue-400/30',
    secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700',
    danger: 'bg-red-600 hover:bg-red-500 text-white shadow-red-500/20 border border-red-400/30',
    warning: 'bg-amber-600 hover:bg-amber-500 text-white shadow-amber-500/20 border border-amber-400/30',
    purple: 'bg-purple-600 hover:bg-purple-500 text-white shadow-purple-500/20 border border-purple-400/30',
  };

  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      className={`${baseStyle} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  );
};
