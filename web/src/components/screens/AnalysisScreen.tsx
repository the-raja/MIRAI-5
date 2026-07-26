'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

const ANALYSIS_STEPS = [
  '🔍 Scanning Player Stance & Combat History...',
  '🧠 Processing XGBoost Intent Prediction & Temporal LSTM...',
  '⚠️ Evaluating 17-Feature Threat Ranking Model...',
  '💾 Searching Vector Memory (Retrieving Episode 102)...',
  '🎯 Synthesizing HTN Task Network & Counter Strategy...',
  '⚡ Counter Strategy Locked. Preparing Arena...'
];

export default function AnalysisScreen() {
  const { setScreen, selectedHero, strategyChoice } = useMiraiStore();
  const [stepIdx, setStepIdx] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setStepIdx((prev) => {
        if (prev < ANALYSIS_STEPS.length - 1) {
          return prev + 1;
        } else {
          clearInterval(timer);
          setTimeout(() => setScreen('battle'), 1000);
          return prev;
        }
      });
    }, 900);

    return () => clearInterval(timer);
  }, [setScreen]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-950 text-white p-8 select-none">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-lg bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-2xl p-8 text-center shadow-2xl flex flex-col items-center"
      >
        <div className="relative w-24 h-24 mb-6 flex items-center justify-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            className="absolute inset-0 border-4 border-blue-500/20 border-t-blue-500 rounded-full"
          />
          <span className="text-3xl">🔮</span>
        </div>

        <h2 className="text-2xl font-bold text-slate-100 mb-2">MIRAI ANALYSIS</h2>
        <p className="text-xs font-mono text-blue-400 mb-6">HERO: {selectedHero} | STANCE: {strategyChoice}</p>

        <div className="w-full bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-emerald-400 min-h-[60px] flex items-center justify-center">
          <motion.span key={stepIdx} initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }}>
            {ANALYSIS_STEPS[stepIdx]}
          </motion.span>
        </div>
      </motion.div>
    </div>
  );
}
