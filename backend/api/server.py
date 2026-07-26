"""FastAPI Server for Phase 0 Backend Freeze.

Finalized Server entrypoint serving:
- REST API routes (/api/...)
- Real-time WebSocket event stream (/ws)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router as api_router
from backend.api.websocket_manager import WebSocketManager

app = FastAPI(title="MIRAI v2 Cognitive OS API", version="2.0.0")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ws_manager = WebSocketManager()

app.include_router(api_router, prefix="/api")


@app.get("/")
def root_status():
    return {"status": "MIRAI v2 API Server Active", "version": "2.0.0"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or process incoming telemetry
            await websocket.send_text(f"Telemetry Received: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
