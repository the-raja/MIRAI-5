import { Howl } from 'howler';

export class AudioService {
  private static instance: AudioService;
  private sounds: Record<string, Howl> = {};
  public isMuted: boolean = false;

  private constructor() {
    this.initDefaultSFX();
  }

  public static getInstance(): AudioService {
    if (!AudioService.instance) {
      AudioService.instance = new AudioService();
    }
    return AudioService.instance;
  }

  private initDefaultSFX() {
    // Synthetic Web Audio / Howler sound triggers for Agent & MIRAI audio events
    const createSynthBeep = (freq: number, type: OscillatorType = 'sine') => {
      if (typeof window === 'undefined') return;
      try {
        const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
      } catch (e) {
        // Fallback
      }
    };

    this.sounds = {
      thinking: { play: () => createSynthBeep(440, 'sine') } as any,
      prediction: { play: () => createSynthBeep(880, 'triangle') } as any,
      learning: { play: () => createSynthBeep(520, 'square') } as any,
      attack: { play: () => createSynthBeep(300, 'sawtooth') } as any,
      heal: { play: () => createSynthBeep(600, 'sine') } as any,
      ultimate: { play: () => createSynthBeep(950, 'sawtooth') } as any,
    };
  }

  public playSound(soundKey: string) {
    if (this.isMuted) return;
    if (this.sounds[soundKey]) {
      this.sounds[soundKey].play();
    }
  }
}

export const audioService = AudioService.getInstance();
