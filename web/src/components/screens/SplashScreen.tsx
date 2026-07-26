'use client';

import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

export default function SplashScreen() {
  const setScreen = useMiraiStore((state) => state.setScreen);

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-slate-950 text-white overflow-hidden select-none">
      {/* Dynamic Animated Glowing Background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-900/30 via-slate-950 to-slate-950 pointer-events-none" />
      <div className="absolute w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />

      {/* Main Content Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1 }}
        className="relative z-10 flex flex-col items-center text-center p-8 max-w-lg"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          className="w-24 h-24 mb-6 border-2 border-blue-500/40 border-t-blue-500 rounded-full flex items-center justify-center shadow-lg shadow-blue-500/20"
        >
          <span className="text-3xl">🧠</span>
        </motion.div>

        <h1 className="text-6xl font-extrabold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-500 mb-2 drop-shadow-lg">
          MIRAI
        </h1>
        <p className="text-xl font-light text-slate-400 italic mb-10 tracking-wide">
          "I've been waiting."
        </p>

        <motion.button
          whileHover={{ scale: 1.05, boxShadow: '0 0 25px rgba(59, 130, 246, 0.5)' }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setScreen('name_entry')}
          className="px-10 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-lg rounded-xl shadow-xl border border-blue-400/30 transition-all duration-300 tracking-wider"
        >
          ENTER THE CORE
        </motion.button>
      </motion.div>
    </div>
  );
}
