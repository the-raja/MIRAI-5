'use client';

import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

export default function HomeScreen() {
  const { playerName, setScreen } = useMiraiStore();

  const menuItems = [
    { label: '🎮 PLAY BATTLE', desc: 'Enter Combat Arena against MIRAI Boss AI', screen: 'hero_select', color: 'from-blue-600 to-indigo-600' },
    { label: '🧠 BRAIN ARCHIVE', desc: 'Inspect Interactive Cognitive Graph & Subsystems', screen: 'brain_view', color: 'from-purple-600 to-pink-600' },
    { label: '🎬 REPLAY VIEWER', desc: 'Debug Past Matches Frame-by-Frame', screen: 'replay', color: 'from-emerald-600 to-teal-600' },
    { label: '📊 STATISTICS & BENCHMARKS', desc: 'View 5,000-Match Empirical Metrics & Ablation', screen: 'learning', color: 'from-amber-600 to-orange-600' },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-white p-8 select-none">
      {/* Top Navbar */}
      <header className="flex justify-between items-center pb-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse shadow-lg shadow-emerald-500/50" />
          <h1 className="text-2xl font-extrabold tracking-wider text-blue-400">MIRAI v2 CORE</h1>
        </div>
        <div className="text-sm font-mono text-slate-400 bg-slate-900 px-4 py-2 rounded-xl border border-slate-800">
          OPERATOR: <span className="text-blue-400 font-bold">{playerName}</span>
        </div>
      </header>

      {/* Main Command Center Grid */}
      <main className="flex-1 flex flex-col items-center justify-center max-w-4xl mx-auto w-full py-10">
        <h2 className="text-4xl font-extrabold mb-2 tracking-wide text-slate-100">COMMAND CENTER</h2>
        <p className="text-slate-400 text-sm mb-8">Select an Operational Command to Initiate</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 w-full">
          {menuItems.map((item, idx) => (
            <motion.div
              key={idx}
              whileHover={{ scale: 1.03, y: -2 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setScreen(item.screen as any)}
              className={`p-6 rounded-2xl bg-gradient-to-r ${item.color} cursor-pointer border border-white/10 shadow-xl transition-all duration-300 flex flex-col justify-between`}
            >
              <div>
                <h3 className="text-xl font-bold text-white mb-2">{item.label}</h3>
                <p className="text-xs text-white/80 leading-relaxed">{item.desc}</p>
              </div>
              <div className="mt-4 text-xs font-mono text-white/60 text-right">EXECUTE ➔</div>
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  );
}
