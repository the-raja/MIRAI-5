'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

const LEARNING_STEPS = [
  '⚔️ Battle Finished (Session battle_01 Finalized)',
  '💾 Episode Saved to Vector Storage',
  '🧠 Multi-Tier Memory Graph Updated',
  '📜 Planner v2 Task Decomposition Adjusted',
  '🔮 Prediction Fusion Weights Improved',
  '💾 Brain Checkpoint Saved (v3.2 Registered)'
];

export default function LearningScreen() {
  const setScreen = useMiraiStore((state) => state.setScreen);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => {
        if (prev < LEARNING_STEPS.length - 1) {
          return prev + 1;
        } else {
          clearInterval(timer);
          return prev;
        }
      });
    }, 800);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-white p-8 select-none">
      <header className="flex justify-between items-center pb-4 border-b border-slate-800">
        <button onClick={() => setScreen('home')} className="text-sm font-mono text-slate-400 hover:text-white">
          ➔ BACK TO HOME
        </button>
        <h2 className="text-xl font-bold text-amber-400">CONTINUOUS ONLINE LEARNING</h2>
        <div className="w-20" />
      </header>

      <main className="flex-1 flex flex-col items-center justify-center max-w-4xl mx-auto w-full py-6">
        <div className="w-full bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-2xl p-8 shadow-2xl mb-6 text-center">
          <h3 className="text-2xl font-bold text-slate-100 mb-6">POST-MATCH LEARNING PIPELINE</h3>

          <div className="space-y-3 font-mono text-xs max-w-xl mx-auto text-left mb-8">
            {LEARNING_STEPS.map((step, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -10 }}
                animate={{
                  opacity: idx <= activeStep ? 1 : 0.3,
                  x: idx <= activeStep ? 0 : -10,
                }}
                className={`p-3.5 rounded-xl border flex items-center justify-between ${
                  idx === activeStep
                    ? 'bg-amber-500/20 border-amber-500 text-amber-300 font-bold'
                    : idx < activeStep
                    ? 'bg-slate-950 border-emerald-500/40 text-emerald-400'
                    : 'bg-slate-950 border-slate-800 text-slate-600'
                }`}
              >
                <span>{step}</span>
                {idx < activeStep ? <span>✓ DONE</span> : idx === activeStep ? <span className="animate-pulse">PROCESSING...</span> : <span>PENDING</span>}
              </motion.div>
            ))}
          </div>

          <button
            onClick={() => setScreen('home')}
            className="px-8 py-3.5 bg-gradient-to-r from-amber-600 to-orange-600 text-white font-bold text-sm rounded-xl shadow-lg hover:from-amber-500 hover:to-orange-500"
          >
            RETURN TO COMMAND CENTER ➔
          </button>
        </div>
      </main>
    </div>
  );
}
