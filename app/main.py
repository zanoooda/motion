
import os, time, cv2
from datetime import datetime

cap = cv2.VideoCapture(0)
ok, frame = cap.read()
if not ok:
    raise RuntimeError("Cannot read from source")

bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
bg = cv2.GaussianBlur(bg, (21, 21), 0)

last_saved = 0.0

while True:
    ok, frame = cap.read()
    if not ok:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    diff = cv2.absdiff(bg, gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    changed = cv2.countNonZero(thresh)
    now = time.time()
    if changed > 5000 and (now - last_saved) >= 1.0:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        path = os.path.join("/data", f"motion_{ts}.jpg")
        cv2.imwrite(path, frame)
        print(f"[motion] saved: {path} (changed={changed})")
        last_saved = now

    bg = gray

cap.release()
