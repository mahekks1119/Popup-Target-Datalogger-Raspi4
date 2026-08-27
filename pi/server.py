"""
Raspberry Pi WebSocket Server — Stage 1 POC

Runs a WebSocket server that:
  1. Broadcasts dummy data typed into this terminal (stdin) to any connected
     GUI clients (laptop/tablet browser). This stands in for real bullet-hit
     sensor data until that hardware/logic is decided.
  2. Receives motor rotation commands from connected GUI clients and hands
     them off to motor_control.py (currently stubbed — no GPIO wiring yet).

Run (on the Pi, inside the venv):
    source ~/gpio-env/bin/activate
    python3 server.py

Then open gui/index.html in a laptop browser and point it at:
    ws://msraspi4.local:8765
"""

import asyncio
import json
from datetime import datetime, timezone

import websockets
from websockets.server import WebSocketServerProtocol

import motor_control

HOST = "0.0.0.0"      # listen on all interfaces on the Pi's WiFi
PORT = 8765

# Every currently-connected GUI client, so we can broadcast to all of them
connected_clients: set[WebSocketServerProtocol] = set()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def broadcast(message: dict) -> None:
    """Send a JSON message to every connected GUI client."""
    if not connected_clients:
        return
    payload = json.dumps(message)
    # gather with return_exceptions so one slow/dead client doesn't block the rest
    await asyncio.gather(
        *(client.send(payload) for client in connected_clients),
        return_exceptions=True,
    )


async def handle_client_message(raw_message: str) -> None:
    """Handle a single JSON message received from a GUI client."""
    try:
        data = json.loads(raw_message)
    except json.JSONDecodeError:
        print(f"[server] Ignored non-JSON message from GUI: {raw_message!r}")
        return

    msg_type = data.get("type")

    if msg_type == "motor_command":
        motor = data.get("motor")
        action = data.get("action")
        status = motor_control.handle_motor_command(motor, action)

        await broadcast({
            "type": "motor_ack",
            "motor": motor,
            "action": action,
            "status": status,
            "timestamp": _now_iso(),
        })
    else:
        print(f"[server] Unknown message type from GUI: {msg_type!r}")


async def client_handler(websocket: WebSocketServerProtocol) -> None:
    """One coroutine instance per connected GUI client."""
    connected_clients.add(websocket)
    client_addr = websocket.remote_address
    print(f"[server] GUI client connected: {client_addr}")

    try:
        async for raw_message in websocket:
            await handle_client_message(raw_message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"[server] GUI client disconnected: {client_addr}")


async def terminal_input_loop() -> None:
    """
    Reads dummy data typed into this Pi's SSH terminal and broadcasts it to
    all connected GUI clients.
    """
    while True:
        # input() is blocking — run it in a worker thread so it doesn't
        # freeze the asyncio event loop / WebSocket server.
        value = await asyncio.to_thread(input, "Enter dummy data > ")

        if value.strip() == "":
            continue

        message = {
            "type": "dummy_data",
            "value": value,
            "timestamp": _now_iso(),
        }
        await broadcast(message)
        print(f"[server] Broadcast to {len(connected_clients)} client(s): {value!r}")


async def main() -> None:
    print(f"[server] Starting WebSocket server on ws://{HOST}:{PORT}")
    async with websockets.serve(client_handler, HOST, PORT):
        await terminal_input_loop()  # runs forever, alongside the server


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[server] Shutting down.")
