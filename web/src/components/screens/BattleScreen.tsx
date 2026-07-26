'use client';

import { motion } from 'framer-motion';
import { useMiraiStore } from '@/store/useMiraiStore';
import Arena3D from '@/game/3d/Arena3D';
import { MiraiConnector } from '@/services/miraiConnector';
import { HealthBar } from '@/components/ui/HealthBar';
import { Button } from '@/components/ui/Button';

export default function BattleScreen() {
  const store = useMiraiStore();

  const handleAction = async (act: string) => {
    await MiraiConnector.executePlayerActionAndReceiveBossDecision(act);
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-white p-6 select-none">
      <header className="flex justify-between items-center pb-4 border-b border-slate-800 mb-4">
        <div className="flex items-center gap-3">
          <span className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse" />
          <h2 className="text-lg font-bold text-slate-100">3D COMBAT ARENA</h2>
        </div>
        <div className="flex gap-3">
          <button onClick={() => store.setScreen('brain_view')} className="px-4 py-2 bg-purple-600/30 border border-purple-500 text-purple-300 font-mono text-xs rounded-xl hover:bg-purple-600/50">
            🧠 BRAIN VIEW
          </button>
          <button onClick={() => store.setScreen('home')} className="px-4 py-2 bg-slate-800 text-slate-300 text-xs rounded-xl hover:bg-slate-700">
            PAUSE / EXIT
          </button>
        </div>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        {/* Left 3D Arena Column */}
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <HealthBar label="Boss HP (MIRAI AI)" currentHp={store.bossHp} variant="boss" />
            <HealthBar label={`Player HP (${store.playerName})`} currentHp={store.playerHp} variant="player" />
          </div>

          <Arena3D />

          <div className="mt-4 grid grid-cols-3 md:grid-cols-6 gap-2">
            <Button variant="primary" onClick={() => handleAction('BasicAttack')}>Attack</Button>
            <Button variant="danger" onClick={() => handleAction('HeavyAttack')}>Heavy</Button>
            <Button variant="warning" onClick={() => handleAction('Dash')}>Dash</Button>
            <Button variant="secondary" onClick={() => handleAction('Heal')}>Heal</Button>
            <Button variant="purple" onClick={() => handleAction('Ultimate')}>Ultimate</Button>
            <Button variant="secondary" onClick={() => handleAction('Death')}>Yield</Button>
          </div>
        </div>

        {/* Right XAI Thinking Panel */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
          <div>
            <h3 className="text-base font-bold text-blue-400 mb-1 flex items-center gap-2">
              <span>🧠</span> LIVE AI REASONING PANEL
            </h3>
            <p className="text-xs text-slate-400 mb-4">"Watch the AI Think"</p>

            <div className="space-y-3 font-mono text-xs">
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
                <span className="text-slate-400">🔮 Prediction</span>
                <span className="text-emerald-400 font-bold">{store.predictedIntent} ({store.predictionConfidence * 100}%)</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
                <span className="text-slate-400">🎯 Goal</span>
                <span className="text-blue-400 font-bold">{store.activeGoal}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
                <span className="text-slate-400">📜 Plan</span>
                <span className="text-amber-400 font-bold">{store.activePlan.join(' ➔ ')}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
                <span className="text-slate-400">⚠️ Threat Score</span>
                <span className="text-red-400 font-bold">Healing = {store.threatScore}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
                <span className="text-slate-400">💾 Retrieved Memory</span>
                <span className="text-purple-400 font-bold">{store.retrievedMemory}</span>
              </div>
              <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex justify-between items-center">
                <span className="text-slate-400">⭐ Skill Rating</span>
                <span className="text-indigo-400 font-bold">{store.playerSkillTier} ({store.playerSkillScore})</span>
              </div>
            </div>
          </div>

          <div className="mt-4 bg-blue-600/20 border border-blue-500/40 p-4 rounded-xl text-center">
            <span className="text-xs text-blue-300 block mb-1">FINAL BOSS ACTION</span>
            <span className="text-xl font-bold font-mono text-white">{store.lastBossAction}</span>
          </div>
        </div>
      </main>
    </div>
  );
}
