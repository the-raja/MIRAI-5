'use client';

import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

const STRATEGIES = [
  { id: 'aggression', name: 'Aggression', desc: 'Continuous close-range pressure, heavy attack priority.', icon: '⚡' },
  { id: 'retreat', name: 'Retreat & Kiting', desc: 'Maintain safe distance, counter on reload attempts.', icon: '🏹' },
  { id: 'protect', name: 'Protect & Shield', desc: 'Focus on defensive blocking, energy regeneration.', icon: '🛡️' },
  { id: 'focus', name: 'Focus Burst', desc: 'Wait for high-confidence prediction windows for ultimate strikes.', icon: '🎯' },
  { id: 'formation', name: 'Tactical Formation', desc: 'Balanced utility AI positioning and pillar usage.', icon: '📐' },
];

export default function StrategyScreen() {
  const { strategyChoice, setStrategyChoice, setScreen } = useMiraiStore();

  const handleSelect = (stratName: string) => {
    setStrategyChoice(stratName);
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-white p-8 select-none">
      <header className="flex justify-between items-center pb-4 border-b border-slate-800">
        <button onClick={() => setScreen('hero_select')} className="text-sm font-mono text-slate-400 hover:text-white">
          ➔ BACK TO HERO SELECT
        </button>
        <h2 className="text-xl font-bold text-blue-400">STRATEGY PLANNING</h2>
        <div className="w-20" />
      </header>

      <main className="flex-1 flex flex-col items-center justify-center max-w-4xl mx-auto w-full py-6">
        <h2 className="text-3xl font-extrabold mb-2 text-slate-100">CONFIGURE TACTICAL DIRECTIVE</h2>
        <p className="text-slate-400 text-sm mb-8">MIRAI Boss AI will build dynamic counters against your chosen stance</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full mb-8">
          {STRATEGIES.map((s) => (
            <motion.div
              key={s.id}
              whileHover={{ scale: 1.02 }}
              onClick={() => handleSelect(s.name)}
              className={`p-5 rounded-xl border cursor-pointer transition-all flex items-start gap-4 ${
                strategyChoice === s.name
                  ? 'bg-blue-600/20 border-blue-500 shadow-lg shadow-blue-500/20'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <span className="text-3xl">{s.icon}</span>
              <div>
                <h3 className="font-bold text-slate-100 mb-1">{s.name}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{s.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setScreen('analysis')}
          className="px-10 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-lg rounded-xl shadow-xl"
        >
          INITIATE MIRAI ANALYSIS ➔
        </motion.button>
      </main>
    </div>
  );
}
