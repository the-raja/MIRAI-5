import { useMiraiStore } from '@/store/useMiraiStore';

class WebSocketService {
  private socket: WebSocket | null = null;
  private url: string = 'ws://localhost:8000/ws';

  public connect() {
    try {
      this.socket = new WebSocket(this.url);

      this.socket.onopen = () => {
        console.log('Connected to MIRAI Telemetry WebSocket Stream');
      };

      this.socket.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.data) {
            useMiraiStore.getState().updateBattleTelemetry({
              playerHp: payload.data.player_hp ?? 100,
              bossHp: payload.data.boss_hp ?? 100,
              lastBossAction: payload.data.boss_action ?? 'Dash',
              lastPlayerAction: payload.data.player_action ?? 'Attack',
              threatScore: payload.data.threat_update?.healing ?? 0.91,
              predictedIntent: payload.data.prediction_update?.intent ?? 'Reload',
              predictionConfidence: payload.data.prediction_update?.confidence ?? 0.94,
              dominantEmotion: payload.data.emotion_update ?? 'Aggressive',
              retrievedMemory: payload.data.memory_trigger ?? 'Episode 102',
              activeGoal: payload.data.planner_change ?? 'Pressure Player',
            });
          }
        } catch (e) {
          // Ignore non-JSON messages
        }
      };

      this.socket.onclose = () => {
        console.log('MIRAI WebSocket disconnected, retrying in 3s...');
        setTimeout(() => this.connect(), 3000);
      };
    } catch (e) {
      console.warn('WebSocket connection error:', e);
    }
  }

  public sendAction(action: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ action, timestamp: Date.now() }));
    }
  }
}

export const wsService = new WebSocketService();
