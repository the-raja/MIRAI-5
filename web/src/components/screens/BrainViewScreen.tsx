'use client';

import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

export default function BrainViewScreen() {
  const setScreen = useMiraiStore((state) => state.setScreen);

  const nodes = [
    { id: 'perception', name: 'Perception Engine', desc: 'Entity Tracking & Frame Buffer', status: 'ACTIVE', color: 'border-blue-500 text-blue-400' },
    { id: 'memory', name: 'Vector Memory Store', desc: 'Dense Summary Embeddings (1,000 Exp)', status: 'ACTIVE', color: 'border-purple-500 text-purple-400' },
    { id: 'prediction', name: 'Prediction Fusion Engine', desc: 'XGBoost (91%) + LSTM (96%)', status: 'ACTIVE', color: 'border-emerald-500 text-emerald-400' },
    { id: 'threat', name: 'Threat Ranking Engine', desc: '17-Feature XGBoost Threat Evaluator', status: 'ACTIVE', color: 'border-red-500 text-red-400' },
    { id: 'planner', name: 'Planner v2 (HTN + BT)', desc: 'Hierarchical Task Network & BT Execution', status: 'ACTIVE', color: 'border-amber-500 text-amber-400' },
    { id: 'decision', name: 'Decision Cortex & Utility', desc: 'Multi-Attribute Utility Maximization', status: 'ACTIVE', color: 'border-cyan-500 text-cyan-400' },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-white p-8 select-none">
      <header className="flex justify-between items-center pb-4 border-b border-slate-800">
        <button onClick={() => setScreen('battle')} className="text-sm font-mono text-slate-400 hover:text-white">
          ➔ BACK TO BATTLE
        </button>
        <h2 className="text-xl font-bold text-purple-400">BRAIN ARCHIVE & COGNITIVE GRAPH</h2>
        <div className="w-20" />
      </header>

      <main className="flex-1 flex flex-col items-center justify-center max-w-5xl mx-auto w-full py-6">
        <h2 className="text-3xl font-extrabold mb-2 text-slate-100">LIVE COGNITIVE SUBSYSTEM FLOW</h2>
        <p className="text-slate-400 text-sm mb-8">Real-time node status and graph activations across MIRAI OS</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mb-8">
          {nodes.map((n) => (
            <motion.div
              key={n.id}
              whileHover={{ scale: 1.03 }}
              className={`p-5 rounded-2xl bg-slate-900/80 backdrop-blur-xl border ${n.color} shadow-xl flex flex-col justify-between`}
            >
              <div>
                <span className="text-xs font-mono bg-slate-950 px-2.5 py-1 rounded-md border border-slate-800 text-emerald-400 inline-block mb-3">
                  {n.status}
                </span>
                <h3 className="text-lg font-bold mb-1">{n.name}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{n.desc}</p>
              </div>
              <div className="mt-4 text-xs font-mono text-slate-500 text-right">LATENCY: 0.4ms</div>
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  );
}
