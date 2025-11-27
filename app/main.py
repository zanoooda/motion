
import os, time, cv2
from datetime import datetime
from config import MOTION_THRESHOLD, SAVE_COOLDOWN_SECONDS, OUTPUT_DIR, CAMERA_INDEX, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from notifiers.telegram import TelegramNotifier

cap = cv2.VideoCapture(CAMERA_INDEX)
ok, frame = cap.read()
if not ok:
    raise RuntimeError("Cannot read from source")

bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
bg = cv2.GaussianBlur(bg, (21, 21), 0)

last_saved = 0.0

notifier = TelegramNotifier(token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)

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
    
    print(f"changed={changed}")
    if changed > MOTION_THRESHOLD and (now - last_saved) >= SAVE_COOLDOWN_SECONDS:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
        path = os.path.join(OUTPUT_DIR, f"motion_{ts}.jpg")
        cv2.imwrite(path, frame)
        print(f"[motion] saved: {path} (changed={changed})")
        last_saved = now
        notifier.send_notification(photo_path=path, caption=f"Motion detected! Saved image: {path} (changed={changed})")

    bg = gray

cap.release()
