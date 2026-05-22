import cv2
import time

# =========================================
# LOAD HAAR CASCADES
# =========================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)6

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_eye.xml'
)

# =========================================
# OPEN CAMERA (Raspberry Pi)
# =========================================

cap = cv2.VideoCapture(0)

# Lower resolution for better performance
cap.set(3, 320)
cap.set(4, 240)

# =========================================
# VARIABLES
# =========================================

# Eye timer
eyes_closed_start = None

# Head movement
normal_center_y = None
head_down_start = None

print("Sleep Detection System Started")

# =========================================
# MAIN LOOP
# =========================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # =========================================
    # FACE DETECTION
    # =========================================

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        # Draw face rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        # =========================================
        # HEAD DOWN DETECTION
        # =========================================

        center_y = y + h // 2

        # Draw center point
        cv2.circle(
            frame,
            (x + w // 2, center_y),
            5,
            (0, 255, 0),
            -1
        )

        # Save normal head position
        if normal_center_y is None:
            normal_center_y = center_y
            print("Normal head position saved")

        difference = center_y - normal_center_y

        threshold = 40

        # Draw threshold line
        cv2.line(
            frame,
            (0, normal_center_y + threshold),
            (320, normal_center_y + threshold),
            (0, 255, 255),
            2
        )

        # Show movement difference
        cv2.putText(
            frame,
            f"Head Diff: {difference}",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )

        # Detect head down
        if difference > threshold:

            if head_down_start is None:
                head_down_start = time.time()

            head_elapsed = time.time() - head_down_start

            cv2.putText(
                frame,
                f"HEAD DOWN {int(head_elapsed)}s",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            # Sleep detection by head
            if head_elapsed > 2:

                cv2.putText(
                    frame,
                    "SLEEP DETECTED",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    3
                )

                print("HEAD_DOWN_SLEEP")

        else:
            head_down_start = None

        # =========================================
        # EYE DETECTION
        # =========================================

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Draw eyes
        for (ex, ey, ew, eh) in eyes:

            cv2.rectangle(
                roi_color,
                (ex, ey),
                (ex + ew, ey + eh),
                (0, 255, 0),
                2
            )

        # Eyes open
        if len(eyes) > 0:

            eyes_closed_start = None

            cv2.putText(
                frame,
                "EYES OPEN",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # Eyes closed
        else:

            if eyes_closed_start is None:
                eyes_closed_start = time.time()

            eye_elapsed = time.time() - eyes_closed_start

            cv2.putText(
                frame,
                f"EYES CLOSED {int(eye_elapsed)}s",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

            # Sleep detection by eyes
            if eye_elapsed > 3:

                cv2.putText(
                    frame,
                    "SLEEP DETECTED",
                    (10, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    3
                )

                print("EYES_CLOSED_SLEEP")

    # =========================================
    # SHOW WINDOW
    # =========================================

    cv2.imshow("Raspberry Pi Sleep Detection", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =========================================
# CLEANUP
# =========================================

cap.release()
cv2.destroyAllWindows()