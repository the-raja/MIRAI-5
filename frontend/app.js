// MIRAI v2 — Developer Tools & Visualization Suite Client

const memoryData = {
  working: {
    "active_entities": ["player_raja_01"],
    "attention_focus": "player_raja_01",
    "distance": "4.5m",
    "player_hp": "34%"
  },
  episodic: {
    "total_episodes": 42,
    "last_episode_id": "ep_102",
    "duration_sec": 34.5,
    "outcome": "VICTORY"
  },
  semantic: {
    "learned_rules": [
      "Player reloads after 3 consecutive attacks (Conf 91%)",
      "Player dodges left under 30% HP (Conf 88%)"
    ]
  },
  vector: {
    "indexed_experiences": 1000,
    "top_similarity_match": "Episode 102 (0.94 Cosine)",
    "retrieval_latency": "0.45 ms"
  }
};

function selectMemoryTab(tabName) {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(t => t.classList.remove('active'));
  event.target.classList.add('active');

  const content = document.getElementById('memory-tab-content');
  content.innerHTML = `<pre>${JSON.stringify(memoryData[tabName], null, 2)}</pre>`;
}

function updateReplayFrame(val) {
  document.getElementById('frame-lbl').innerText = `Frame: ${val} / 300`;
  const box = document.getElementById('replay-box');
  
  if (val > 150) {
    box.innerHTML = `
      <div class="audit-row"><strong>Target Action:</strong> Interrupt Reload</div>
      <div class="audit-row"><strong>Fused Prediction:</strong> Reload (94% Conf)</div>
      <div class="audit-row"><strong>Retrieved Vector Match:</strong> Episode 102 (Cosine 0.94)</div>
      <div class="audit-row"><strong>Audit Reasoning:</strong> "Player reloads under pressure. Replanned Goal: Pressure Heal."</div>
    `;
  } else {
    box.innerHTML = `
      <div class="audit-row"><strong>Target Action:</strong> Heavy Attack</div>
      <div class="audit-row"><strong>Fused Prediction:</strong> DodgeLeft (86% Conf)</div>
      <div class="audit-row"><strong>Retrieved Vector Match:</strong> Episode 58 (Cosine 0.91)</div>
      <div class="audit-row"><strong>Audit Reasoning:</strong> "Observed in 78 similar historical sequences."</div>
    `;
  }
}

// Default initialization
document.addEventListener('DOMContentLoaded', () => {
  const content = document.getElementById('memory-tab-content');
  content.innerHTML = `<pre>${JSON.stringify(memoryData.working, null, 2)}</pre>`;
});
