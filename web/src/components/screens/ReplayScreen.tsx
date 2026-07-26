'use client';

import { useMiraiStore } from '@/store/useMiraiStore';

export default function ReplayScreen() {
  const { replayFrame, setReplayFrame, setScreen } = useMiraiStore();

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-white p-8 select-none">
      <header className="flex justify-between items-center pb-4 border-b border-slate-800">
        <button onClick={() => setScreen('home')} className="text-sm font-mono text-slate-400 hover:text-white">
          ➔ BACK TO HOME
        </button>
        <h2 className="text-xl font-bold text-emerald-400">REPLAY VIEWER & AI FRAME DEBUGGER</h2>
        <div className="w-20" />
      </header>

      <main className="flex-1 flex flex-col items-center justify-center max-w-4xl mx-auto w-full py-6">
        <div className="w-full bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 shadow-2xl">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold text-slate-100">MATCH REPLAY SCRUBBER</h3>
            <span className="text-sm font-mono text-emerald-400 bg-slate-950 px-3 py-1 rounded-lg border border-slate-800">
              FRAME: {replayFrame} / 300
            </span>
          </div>

          <input
            type="range"
            min="1"
            max="300"
            value={replayFrame}
            onChange={(e) => setReplayFrame(parseInt(e.target.value))}
            className="w-full accent-emerald-500 mb-8 cursor-pointer"
          />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-500 block mb-1">PREDICTION AT FRAME {replayFrame}</span>
              <span className="text-emerald-400 font-bold text-sm">Reload (94%)</span>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-500 block mb-1">THREAT RANKING</span>
              <span className="text-red-400 font-bold text-sm">Healing = 0.91</span>
            </div>
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <span className="text-slate-500 block mb-1">DECISION AUDIT</span>
              <span className="text-blue-400 font-bold text-sm">Dash ➔ Heavy Attack</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
