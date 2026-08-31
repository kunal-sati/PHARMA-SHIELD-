import json
import asyncio
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["WebSockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

ws_manager = ConnectionManager()

@router.websocket("/ws/shipments/{shipment_id}")
async def websocket_shipment_stream(websocket: WebSocket, shipment_id: str):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Heartbeat ping/pong loop
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"event": "pong", "shipment_id": shipment_id})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
