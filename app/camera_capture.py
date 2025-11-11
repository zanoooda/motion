import os
import time
import signal
import threading
from datetime import datetime
import cv2

# Optional remote debug (VS Code -> Attach)
if os.getenv("DEBUGPY") == "1":
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))

SNAP_INTERVAL = float(os.getenv("SNAP_INTERVAL", "2"))
CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

stop_event = threading.Event()

def sigterm_handler(*_):
    stop_event.set()

signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)

def open_camera(index: int):
    # CAP_V4L2 helps on Linux systems
    cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
    if not cap.isOpened():
        cap = cv2.VideoCapture(index)
    return cap

def capture_loop():
    cap = open_camera(CAMERA_INDEX)
    if not cap.isOpened():
        print(f"[error] Cannot open camera index {CAMERA_INDEX}")
        return

    print(f"[info] Started capture from camera {CAMERA_INDEX}, interval={SNAP_INTERVAL}s, output={OUTPUT_DIR}")

    while not stop_event.is_set():
        ok, frame = cap.read()
        if not ok:
            print("[warn] Failed to read frame; retrying...")
            time.sleep(0.5)
            continue

        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = os.path.join(OUTPUT_DIR, f"frame_{ts}.jpg")
        ok = cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        if not ok:
            print(f"[warn] Failed to write frame to {path}")

        time.sleep(SNAP_INTERVAL)

    cap.release()
    print("[info] Capture stopped.")

def main():
    t = threading.Thread(target=capture_loop, daemon=True)
    t.start()
    try:
        while not stop_event.is_set():
            time.sleep(0.5)
    finally:
        stop_event.set()
        t.join()

if __name__ == "__main__":
    main()
