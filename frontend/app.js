// MIRAI v2 — Demo Game & AI Debugger Vertical Slice Client

let canvas, ctx;
let gameRunning = false;
let isPaused = false;
let currentFrame = 130;

const player = { x: 140, y: 190, radius: 18, hp: 100, color: '#3b82f6', speed: 4 };
const boss = { x: 480, y: 190, radius: 24, hp: 100, color: '#ef4444', speed: 2.5 };
const pillar = { x: 310, y: 140, width: 30, height: 100, color: '#64748b' };
const healthPack = { x: 320, y: 290, radius: 12, color: '#10b981' };

const keys = {};

function initGame() {
  canvas = document.getElementById('combat-canvas');
  ctx = canvas.getContext('2d');

  window.addEventListener('keydown', (e) => { keys[e.key.toLowerCase()] = true; });
  window.addEventListener('keyup', (e) => { keys[e.key.toLowerCase()] = false; });

  drawGame();
}

function startGame() {
  gameRunning = true;
  isPaused = false;
  requestAnimationFrame(gameLoop);
}

function togglePauseGame() {
  isPaused = !isPaused;
}

function resetGame() {
  player.x = 140; player.y = 190; player.hp = 100;
  boss.x = 480; boss.y = 190; boss.hp = 100;
  gameRunning = false;
  isPaused = false;
  updateHUD();
  drawGame();
}

function gameLoop() {
  if (!gameRunning) return;

  if (!isPaused) {
    updateGameLogic();
    currentFrame++;
    if (currentFrame > 300) currentFrame = 1;
    document.getElementById('debugger-scrubber').value = currentFrame;
    updateXAIReasoning(currentFrame);
  }

  drawGame();
  requestAnimationFrame(gameLoop);
}

function updateGameLogic() {
  // Player movement
  if (keys['w'] || keys['arrowup']) player.y = Math.max(30, player.y - player.speed);
  if (keys['s'] || keys['arrowdown']) player.y = Math.min(canvas.height - 30, player.y + player.speed);
  if (keys['a'] || keys['arrowleft']) player.x = Math.max(30, player.x - player.speed);
  if (keys['d'] || keys['arrowright']) player.x = Math.min(canvas.width - 30, player.x + player.speed);

  // Simple Boss AI tracking
  const dx = player.x - boss.x;
  const dy = player.y - boss.y;
  const dist = Math.hypot(dx, dy);

  if (dist > 60) {
    boss.x += (dx / dist) * boss.speed;
    boss.y += (dy / dist) * boss.speed;
  }

  updateHUD();
}

function updateHUD() {
  document.getElementById('boss-hp-fill').style.width = boss.hp + '%';
  document.getElementById('boss-hp-text').innerText = `${boss.hp} / 100`;

  document.getElementById('player-hp-fill').style.width = player.hp + '%';
  document.getElementById('player-hp-text').innerText = `${player.hp} / 100`;
}

function drawGame() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Background grid
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
  ctx.lineWidth = 1;
  for (let x = 0; x < canvas.width; x += 40) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
  }
  for (let y = 0; y < canvas.height; y += 40) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
  }

  // Pillar Obstacle
  ctx.fillStyle = pillar.color;
  ctx.fillRect(pillar.x, pillar.y, pillar.width, pillar.height);

  // Health Pack
  ctx.fillStyle = healthPack.color;
  ctx.beginPath();
  ctx.arc(healthPack.x, healthPack.y, healthPack.radius, 0, Math.PI * 2);
  ctx.fill();

  // Player
  ctx.fillStyle = player.color;
  ctx.beginPath();
  ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#ffffff';
  ctx.font = '12px Inter';
  ctx.fillText('Player', player.x - 18, player.y - 24);

  // Boss AI
  ctx.fillStyle = boss.color;
  ctx.beginPath();
  ctx.arc(boss.x, boss.y, boss.radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#ffffff';
  ctx.font = '12px Inter';
  ctx.fillText('Boss AI', boss.x - 22, boss.y - 30);
}

function updateXAIReasoning(frame) {
  if (frame > 200) {
    document.getElementById('xai-pred').innerHTML = `Ultimate Attack <span class="highlight">(95%)</span>`;
    document.getElementById('xai-goal').innerText = `Punish & Execute`;
    document.getElementById('xai-plan').innerText = `Plan C (Block ➔ Counter)`;
    document.getElementById('xai-threat').innerHTML = `Ultimate = <span class="highlight-red">0.95</span>`;
    document.getElementById('xai-memory').innerText = `Episode 150 (Cosine Sim 0.96)`;
    document.getElementById('xai-action').innerText = `Heavy Attack Counter`;
  } else if (frame > 100) {
    document.getElementById('xai-pred').innerHTML = `Reload <span class="highlight">(94%)</span>`;
    document.getElementById('xai-goal').innerText = `Pressure Player`;
    document.getElementById('xai-plan').innerText = `Plan A (Dash ➔ Heavy Attack)`;
    document.getElementById('xai-threat').innerHTML = `Healing = <span class="highlight-red">0.91</span>`;
    document.getElementById('xai-memory').innerText = `Episode 102 (Cosine Sim 0.94)`;
    document.getElementById('xai-action').innerText = `Dash`;
  } else {
    document.getElementById('xai-pred').innerHTML = `Attack <span class="highlight">(82%)</span>`;
    document.getElementById('xai-goal').innerText = `Maintain Control`;
    document.getElementById('xai-plan').innerText = `Plan B (Positioning)`;
    document.getElementById('xai-threat').innerHTML = `Reload = <span class="highlight-red">0.28</span>`;
    document.getElementById('xai-memory').innerText = `Episode 45 (Cosine Sim 0.88)`;
    document.getElementById('xai-action').innerText = `Block`;
  }
}

function debugFrameScrub(val) {
  currentFrame = parseInt(val);
  document.getElementById('debugger-frame-lbl').innerText = `Frame: ${currentFrame} / 300`;
  updateXAIReasoning(currentFrame);

  const grid = document.getElementById('debugger-trace-grid');
  grid.innerHTML = `
    <div class="trace-cell"><strong>Frame ${currentFrame}</strong> ➔ Snapshot</div>
    <div class="trace-cell"><strong>Prediction:</strong> ${document.getElementById('xai-pred').innerText}</div>
    <div class="trace-cell"><strong>Memory:</strong> ${document.getElementById('xai-memory').innerText}</div>
    <div class="trace-cell"><strong>Threat:</strong> ${document.getElementById('xai-threat').innerText}</div>
    <div class="trace-cell"><strong>Plan:</strong> ${document.getElementById('xai-plan').innerText}</div>
    <div class="trace-cell"><strong>Decision:</strong> ${document.getElementById('xai-action').innerText}</div>
  `;
}

document.addEventListener('DOMContentLoaded', initGame);
