import asyncio
import os
import threading
import json
import time

import cv2
import websockets


HOST = "0.0.0.0"
DEFAULT_PORT = 8765
CAMERA_PATH = "/ws/camera"
JPEG_QUALITY = 70

connected_clients = set()
serial_clients = set()
_loop = None
_server = None
_thread = None
_ready = threading.Event()


async def _handle_client(websocket, path=None):
    request_path = path or getattr(websocket, "path", None)
    if request_path is None and hasattr(websocket, "request"):
        request_path = getattr(websocket.request, "path", None)

    if request_path == CAMERA_PATH:
        connected_clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            connected_clients.discard(websocket)
    else:
        await websocket.close(code=1008, reason="Unsupported path")
        return


async def _start_server():
    global _server

    port = int(os.getenv("WS_PORT", str(DEFAULT_PORT)))
    _server = await websockets.serve(_handle_client, HOST, port)
    print(f"Camera WebSocket server listening on ws://{HOST}:{port}{CAMERA_PATH}")
    _ready.set()


def start_ws_server():
    global _loop, _server

    if _loop is not None:
        return

    _loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_loop)
    try:
        _loop.run_until_complete(_start_server())
        _loop.run_forever()
    finally:
        _loop.close()
        _loop = None
        _server = None
        _ready.clear()


async def _close_clients():
    clients = list(connected_clients)
    if clients:
        await asyncio.gather(
            *(client.close(code=1001, reason="Inference stopped") for client in clients),
            return_exceptions=True,
        )
    connected_clients.clear()

    s_clients = list(serial_clients)
    if s_clients:
        await asyncio.gather(
            *(client.close(code=1001, reason="Inference stopped") for client in s_clients),
            return_exceptions=True,
        )
    serial_clients.clear()

    if _server is not None:
        _server.close()
        await _server.wait_closed()


def stop_ws_server():
    global _loop, _server, _thread

    if _loop is None:
        return

    loop = _loop
    thread = _thread
    future = asyncio.run_coroutine_threadsafe(_close_clients(), _loop)
    try:
        future.result(timeout=5)
    except Exception as exc:
        print(f"Camera WebSocket shutdown failed: {exc}")

    loop.call_soon_threadsafe(loop.stop)
    if thread is not None and thread.is_alive():
        thread.join(timeout=5)
    _loop = None
    _server = None
    _thread = None


def run_ws_server_in_thread():
    global _thread

    if _thread is not None and _thread.is_alive():
        return

    _thread = threading.Thread(target=start_ws_server, daemon=True)
    _thread.start()
    _ready.wait(timeout=5)


async def _broadcast_payload(payload):
    if connected_clients:
        websockets.broadcast(connected_clients, payload)


def broadcast_frame(frame):
    if _loop is None or not connected_clients:
        return

    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
    if not ok:
        return

    asyncio.run_coroutine_threadsafe(_broadcast_payload(buf.tobytes()), _loop)
