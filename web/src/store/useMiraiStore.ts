import { create } from 'zustand';

export type ScreenType =
  | 'splash'
  | 'name_entry'
  | 'home'
  | 'hero_select'
  | 'strategy'
  | 'analysis'
  | 'battle'
  | 'brain_view'
  | 'replay'
  | 'learning';

export interface MiraiState {
  // Game & Navigation
  currentScreen: ScreenType;
  playerName: string;
  selectedHero: string;
  strategyChoice: string;
  isPaused: boolean;
  fps: number;

  // Battle State
  sessionId: string;
  playerHp: number;
  bossHp: number;
  lastPlayerAction: string;
  lastBossAction: string;
  battleStatus: 'IDLE' | 'ACTIVE' | 'VICTORY' | 'DEFEAT';

  // Cognitive Subsystems State
  predictedIntent: string;
  predictionConfidence: number;
  threatScore: number;
  threatDetails: Record<string, number>;
  activeGoal: string;
  activePlan: string[];
  activeBtNode: string;
  retrievedMemory: string;
  playerSkillScore: number;
  playerSkillTier: string;
  dominantEmotion: string;
  emotionArousal: number;

  // Replay & Frame Debugger
  replayFrame: number;

  // Actions
  setScreen: (screen: ScreenType) => void;
  setPlayerName: (name: string) => void;
  setSelectedHero: (hero: string) => void;
  setStrategyChoice: (strategy: string) => void;
  updateBattleTelemetry: (data: Partial<MiraiState>) => void;
  setReplayFrame: (frame: number) => void;
  togglePause: () => void;
  resetBattle: () => void;
}

export const useMiraiStore = create<MiraiState>((set) => ({
  currentScreen: 'splash',
  playerName: 'Raja',
  selectedHero: 'Cyber Knight',
  strategyChoice: 'Aggression',
  isPaused: false,
  fps: 60,

  sessionId: 'battle_01',
  playerHp: 100,
  bossHp: 100,
  lastPlayerAction: 'None',
  lastBossAction: 'Dash',
  battleStatus: 'IDLE',

  predictedIntent: 'Reload',
  predictionConfidence: 0.94,
  threatScore: 0.91,
  threatDetails: { healing: 0.91, ultimate: 0.95 },
  activeGoal: 'Pressure Player',
  activePlan: ['Dash', 'Heavy Attack', 'Block', 'Retreat'],
  activeBtNode: 'SequenceBTNode',
  retrievedMemory: 'Episode 102 (Cosine Sim 0.94)',
  playerSkillScore: 92,
  playerSkillTier: 'Expert',
  dominantEmotion: 'Aggressive',
  emotionArousal: 0.85,

  replayFrame: 130,

  setScreen: (screen) => set({ currentScreen: screen }),
  setPlayerName: (name) => set({ playerName: name }),
  setSelectedHero: (hero) => set({ selectedHero: hero }),
  setStrategyChoice: (strategy) => set({ strategyChoice: strategy }),

  updateBattleTelemetry: (data) => set((state) => ({ ...state, ...data })),

  setReplayFrame: (frame) => set({ replayFrame: frame }),
  togglePause: () => set((state) => ({ isPaused: !state.isPaused })),
  resetBattle: () =>
    set({
      playerHp: 100,
      bossHp: 100,
      lastPlayerAction: 'None',
      lastBossAction: 'Dash',
      battleStatus: 'IDLE',
      isPaused: false,
    }),
}));
