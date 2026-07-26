import { postBattleAction, fetchPredictionState, fetchPlannerState } from './apiService';
import { wsService } from './websocketService';
import { useMiraiStore } from '@/store/useMiraiStore';

export class MiraiConnector {
  public static async executePlayerActionAndReceiveBossDecision(playerAction: string) {
    const store = useMiraiStore.getState();

    // 1. Emit player action to WebSocket stream
    wsService.sendAction(playerAction);

    // 2. Query REST backend for Boss decision (Backend -> Planner -> Decision)
    const backendRes = await postBattleAction(store.sessionId, playerAction);
    const predRes = await fetchPredictionState();
    const planRes = await fetchPlannerState();

    const bossCounter = backendRes?.boss_counter_action || 'Dash';
    const predIntent = predRes?.intent_prediction || 'Reload';
    const predConf = predRes?.confidence || 0.94;
    const planSteps = planRes?.htn_decomposition || ['Reduce HP', 'Pressure', 'Force Reload', 'Punish', 'Retreat'];

    // 3. Update Zustand Store to drive Frontend Animation
    store.updateBattleTelemetry({
      lastPlayerAction: playerAction,
      lastBossAction: bossCounter,
      predictedIntent: predIntent,
      predictionConfidence: predConf,
      activePlan: planSteps,
    });

    return {
      bossCounterAction: bossCounter,
      predictionIntent: predIntent,
      predictionConfidence: predConf,
      planSteps,
    };
  }
}
