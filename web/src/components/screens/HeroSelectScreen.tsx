'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';

const HEROES = [
  { id: 'cyber_knight', name: 'Cyber Knight', role: 'Melee Duelist', hp: '120', speed: 'Fast', ability: 'Plasma Strike', voice: 'Tactical Cyber Voice', desc: 'Agile close-quarters specialist with rapid sword combos.' },
  { id: 'shadow_ninja', name: 'Shadow Ninja', role: 'Assassin', hp: '90', speed: 'Extreme', ability: 'Shadow Step', voice: 'Whispering Blade', desc: 'High mobility flanker specializing in quick dodges and critical strikes.' },
  { id: 'heavy_paladin', name: 'Heavy Paladin', role: 'Tank', hp: '160', speed: 'Slow', ability: 'Aegis Shield', voice: 'Deep Resonant', desc: 'Impenetrable fortress equipped with heavy counter-shields.' },
  { id: 'arcane_mage', name: 'Arcane Mage', role: 'Ranged Caster', hp: '85', speed: 'Medium', ability: 'Arcane Pulse', voice: 'Ethereal Echo', desc: 'Long-range spellcaster manipulating energy bursts and temporal traps.' }
];

export default function HeroSelectScreen() {
  const { selectedHero, setSelectedHero, setScreen } = useMiraiStore();
  const [activeHero, setActiveHero] = useState(HEROES.find(h => h.name === selectedHero) || HEROES[0]);

  const handleSelect = (hero: typeof HEROES[0]) => {
    setActiveHero(hero);
    setSelectedHero(hero.name);
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-white p-8 select-none">
      <header className="flex justify-between items-center pb-4 border-b border-slate-800">
        <button onClick={() => setScreen('home')} className="text-sm font-mono text-slate-400 hover:text-white">
          ➔ BACK TO HOME
        </button>
        <h2 className="text-xl font-bold text-blue-400">AGENT SELECTION</h2>
        <div className="w-20" />
      </header>

      <main className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 py-6 max-w-6xl mx-auto w-full">
        {/* Left Column: Hero List */}
        <div className="flex flex-col gap-3">
          {HEROES.map((h) => (
            <motion.div
              key={h.id}
              whileHover={{ scale: 1.02 }}
              onClick={() => handleSelect(h)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${
                activeHero.id === h.id
                  ? 'bg-blue-600/20 border-blue-500 shadow-lg shadow-blue-500/20'
                  : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex justify-between items-center">
                <h3 className="font-bold text-slate-100">{h.name}</h3>
                <span className="text-xs font-mono text-blue-400">{h.role}</span>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Center/Right Column: Character Viewer & Details */}
        <div className="md:col-span-2 bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <div className="w-full h-48 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-center mb-6">
              <span className="text-6xl">🛡️</span>
            </div>
            <h2 className="text-3xl font-extrabold text-white mb-1">{activeHero.name}</h2>
            <p className="text-xs font-mono text-blue-400 mb-4">{activeHero.role} • Voice: {activeHero.voice}</p>
            <p className="text-sm text-slate-300 mb-6 leading-relaxed">{activeHero.desc}</p>

            <div className="grid grid-cols-3 gap-4 font-mono text-xs text-slate-300">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">BASE HP</span>
                <span className="text-emerald-400 font-bold text-sm">{activeHero.hp}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">SPEED</span>
                <span className="text-blue-400 font-bold text-sm">{activeHero.speed}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <span className="text-slate-500 block">ABILITY</span>
                <span className="text-purple-400 font-bold text-sm">{activeHero.ability}</span>
              </div>
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setScreen('strategy')}
            className="w-full py-4 mt-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-base rounded-xl shadow-lg"
          >
            CONFIRM HERO & STRATEGY ➔
          </motion.button>
        </div>
      </main>
    </div>
  );
}
