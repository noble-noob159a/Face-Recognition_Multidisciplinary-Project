import serial
import os
import threading
from .ws_server import broadcast_serial_line

SERIAL_PORT = os.getenv("YOLOBIT_PORT", "COM3")
SERIAL_BAUD = int(os.getenv("YOLOBIT_BAUD", "115200"))
SERIAL_TIMEOUT = 1

_stop_event = threading.Event()
_thread = None

def _read_loop(stop_event: threading.Event):
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=SERIAL_TIMEOUT)
        print(f"[serial_reader] Opened {SERIAL_PORT} at {SERIAL_BAUD} baud")
    except serial.SerialException as e:
        print(f"[serial_reader] Could not open port: {e}")
        return

    while not stop_event.is_set():
        try:
            raw = ser.readline()
            if not raw:
                continue
            line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            if line:
                broadcast_serial_line(line)
        except serial.SerialException as e:
            print(f"[serial_reader] Serial error: {e}")
            break

    ser.close()
    print("[serial_reader] Port closed.")

def start_serial_reader() -> None:
    global _thread
    if _thread is not None and _thread.is_alive():
        return
    _stop_event.clear()
    _thread = threading.Thread(target=_read_loop, args=(_stop_event,), daemon=True)
    _thread.start()

def stop_serial_reader() -> None:
    global _thread
    _stop_event.set()
    if _thread is not None and _thread.is_alive():
        _thread.join(timeout=5)
    _thread = None
