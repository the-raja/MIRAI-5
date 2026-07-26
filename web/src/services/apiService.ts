const API_BASE_URL = 'http://localhost:8000/api';

export async function fetchSystemState() {
  try {
    const res = await fetch(`${API_BASE_URL}/state`);
    return await res.json();
  } catch (err) {
    console.warn('Backend offline, using fallback state:', err);
    return null;
  }
}

export async function fetchMemoryState() {
  try {
    const res = await fetch(`${API_BASE_URL}/memory`);
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchPredictionState() {
  try {
    const res = await fetch(`${API_BASE_URL}/prediction`);
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchPlannerState() {
  try {
    const res = await fetch(`${API_BASE_URL}/planner`);
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchEmotionState() {
  try {
    const res = await fetch(`${API_BASE_URL}/emotion`);
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function postStartBattle(sessionId: string, playerId: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/battle/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, player_id: playerId }),
    });
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function postBattleAction(sessionId: string, action: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/battle/action`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, action, timestamp: Date.now() / 1000 }),
    });
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function postEndBattle(sessionId: string, outcome: string) {
  try {
    const res = await fetch(`${API_BASE_URL}/battle/end`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, outcome }),
    });
    return await res.json();
  } catch (err) {
    return null;
  }
}
