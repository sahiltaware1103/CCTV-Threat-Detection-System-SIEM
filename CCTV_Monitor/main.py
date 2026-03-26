import cv2
import datetime
import time
import os

# Create snapshots folder
if not os.path.exists("snapshots"):
    os.makedirs("snapshots")

# Logging function
def log_event(event, severity="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"{timestamp} | CCTV | {severity} | {event}"

    with open("alerts.log", "a") as f:
        f.write(log + "\n")

    print("LOG:", log)


# Start camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

last_alert_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ---------------- RED DETECTION ----------------
    lower_red1 = (0, 120, 70)
    upper_red1 = (10, 255, 255)

    lower_red2 = (170, 120, 70)
    upper_red2 = (180, 255, 255)

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_red:
        if cv2.contourArea(contour) < 1000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

        # HIGH severity alert (every 5 sec)
        if time.time() - last_alert_time > 5:
            log_event("Red object detected", "HIGH")

            filename = f"snapshots/red_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)

            last_alert_time = time.time()

    # ---------------- GREEN DETECTION ----------------
    lower_green = (40, 50, 50)
    upper_green = (80, 255, 255)

    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours_green:
        if cv2.contourArea(contour) < 1000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        # NORMAL log (no spam)
        log_event("Green object detected", "INFO")

    # Show video
    cv2.imshow("CCTV Color Detection", frame)

    # Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()