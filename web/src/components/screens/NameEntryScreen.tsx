'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

export default function NameEntryScreen() {
  const { playerName, setPlayerName, setScreen } = useMiraiStore();
  const [nameInput, setNameInput] = useState(playerName);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (nameInput.trim()) {
      setPlayerName(nameInput.trim());
      setScreen('home');
    }
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen bg-slate-950 text-white select-none">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="w-full max-w-md p-8 bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-2xl shadow-2xl text-center"
      >
        <h2 className="text-3xl font-bold text-slate-100 mb-2">IDENTIFY YOURSELF</h2>
        <p className="text-sm text-slate-400 mb-6">Enter your Combat Designation for MIRAI Analysis</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-6">
          <input
            type="text"
            value={nameInput}
            onChange={(e) => setNameInput(e.target.value)}
            placeholder="Enter Designation..."
            className="w-full px-5 py-3.5 bg-slate-950 border border-slate-700 focus:border-blue-500 rounded-xl text-center text-lg text-white font-mono placeholder-slate-600 outline-none transition-all shadow-inner"
            autoFocus
          />

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            className="w-full py-3.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-base rounded-xl shadow-lg transition-all"
          >
            CONTINUE ➔
          </motion.button>
        </form>
      </motion.div>
    </div>
  );
}
