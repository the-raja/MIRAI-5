'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

export default function BrainOverlay() {
  const [isOpen, setIsOpen] = useState(false);
  const store = useMiraiStore();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, backdropFilter: 'blur(0px)' }}
          animate={{ opacity: 1, backdropFilter: 'blur(16px)' }}
          exit={{ opacity: 0, backdropFilter: 'blur(0px)' }}
          className="fixed inset-0 z-50 bg-slate-950/90 text-white p-8 flex flex-col justify-between select-none"
        >
          <div className="flex justify-between items-center pb-4 border-b border-purple-500/30">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🧠</span>
              <h2 className="text-2xl font-extrabold text-purple-400 tracking-wider">
                LIVE BRAIN OVERLAY (TAB TRIGGERED)
              </h2>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-xs font-mono bg-purple-600/30 border border-purple-500 px-4 py-2 rounded-xl text-purple-300 hover:bg-purple-600/50"
            >
              PRESS TAB TO CLOSE ✕
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-auto max-w-6xl mx-auto w-full font-mono text-xs">
            {/* Memory Node */}
            <div className="bg-slate-900/90 border border-purple-500/40 p-5 rounded-2xl shadow-2xl">
              <h3 className="text-sm font-bold text-purple-400 mb-3">💾 VECTOR MEMORY</h3>
              <p className="text-slate-300 mb-2">Retrieved: {store.retrievedMemory}</p>
              <p className="text-slate-400 text-[11px]">Cosine Similarity: 0.94 | Matches: 1,000 Episodes</p>
            </div>

            {/* Planner Node */}
            <div className="bg-slate-900/90 border border-amber-500/40 p-5 rounded-2xl shadow-2xl">
              <h3 className="text-sm font-bold text-amber-400 mb-3">📜 HTN PLANNER v2</h3>
              <p className="text-slate-300 mb-2">Goal: {store.activeGoal}</p>
              <p className="text-amber-300 font-bold">Plan: {store.activePlan.join(' ➔ ')}</p>
            </div>

            {/* Prediction Node */}
            <div className="bg-slate-900/90 border border-emerald-500/40 p-5 rounded-2xl shadow-2xl">
              <h3 className="text-sm font-bold text-emerald-400 mb-3">🔮 PREDICTION FUSION</h3>
              <p className="text-slate-300 mb-2">Intent: {store.predictedIntent}</p>
              <p className="text-emerald-400 font-bold">Confidence: {store.predictionConfidence * 100}%</p>
            </div>

            {/* Threat Node */}
            <div className="bg-slate-900/90 border border-red-500/40 p-5 rounded-2xl shadow-2xl">
              <h3 className="text-sm font-bold text-red-400 mb-3">⚠️ THREAT RANKING</h3>
              <p className="text-slate-300 mb-2">Score: {store.threatScore}</p>
              <p className="text-red-400 font-bold">Top Threat: Healing (0.91)</p>
            </div>

            {/* Emotion Node */}
            <div className="bg-slate-900/90 border border-blue-500/40 p-5 rounded-2xl shadow-2xl">
              <h3 className="text-sm font-bold text-blue-400 mb-3">🎭 EMOTIONAL CORTEX</h3>
              <p className="text-slate-300 mb-2">Emotion: {store.dominantEmotion}</p>
              <p className="text-blue-400 font-bold">Arousal: {store.emotionArousal}</p>
            </div>

            {/* Skill Node */}
            <div className="bg-slate-900/90 border border-indigo-500/40 p-5 rounded-2xl shadow-2xl">
              <h3 className="text-sm font-bold text-indigo-400 mb-3">⭐ PLAYER SKILL</h3>
              <p className="text-slate-300 mb-2">Tier: {store.playerSkillTier}</p>
              <p className="text-indigo-400 font-bold">Score: {store.playerSkillScore} / 100</p>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
