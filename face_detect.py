import cv2
import time
import os

# Global status variable for other modules
CAMERA_STATUS = 0
RUN_CAMERA = True

def get_camera_status():
    return CAMERA_STATUS
def start_camera():
    global RUN_CAMERA
    RUN_CAMERA = True
def stop_camera():
    global RUN_CAMERA
    RUN_CAMERA = False
def CAMERA():
    global CAMERA_STATUS
    global RUN_CAMERA

    RUN_CAMERA = True

    # =========================================
    # LOAD HAAR CASCADES
    # =========================================


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    face_cascade = cv2.CascadeClassifier(
    os.path.join(BASE_DIR, "cascades", "haarcascade_frontalface_default.xml")
    )

    eye_cascade = cv2.CascadeClassifier(
    os.path.join(BASE_DIR, "cascades", "haarcascade_eye.xml")
    )
    # =========================================
    # OPEN CAMERA (Raspberry Pi)
    # =========================================

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    
    cap.set(3, 320)
    cap.set(4, 240)

    # =========================================
    # VARIABLES
    # =========================================

    # Eye timer
    eyes_closed_start = None
    eyes_open_start = None
    face_missing_start = None

    # Head movement
    normal_center_y = None
    head_down_start = None

    # Thresholds
    HEAD_SLEEP_TIME = 4      # seconds
    EYE_SLEEP_TIME = 5      # seconds
    HEAD_THRESHOLD = 15     # pixels

    CAMERA_STATUS = 0

    print("Sleep Detection System Started")

    # =========================================
    # MAIN LOOP
    # =========================================

    while RUN_CAMERA:

        if not RUN_CAMERA:
            time.sleep(0.05)
            continue
        ret, frame = cap.read()

        if not ret:
            print("Camera not detected")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # =========================================
        # FACE DETECTION
        # =========================================

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        # No face detected
        if len(faces) == 0:
            if face_missing_start is None:
                face_missing_start = time.time()
            missing_time = time.time() - face_missing_start

            cv2.putText(
                frame,
                f"FACE LOST {int(missing_time)}s",
                (10, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2 
            )
            if missing_time > 20:
                CAMERA_STATUS = 1
                cv2.putText(
                    frame,
                    "SLEEP DETECTED",
                    (10, 190),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    3
                )
                print("FACE_NOT_DETECTED_SLEEP")

        for (x, y, w, h) in faces:
            face_missing_start = None

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

            threshold = HEAD_THRESHOLD

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

            head_sleep = False

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
                if head_elapsed > HEAD_SLEEP_TIME:

                    CAMERA_STATUS = 1
                    head_sleep = True

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

            # If head sleep detected, skip eye check
            if head_sleep:
                continue

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
                cv2.putText(
                    frame,
                    "EYES OPEN",
                    (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    )

                 # Start eye-open timer
                if eyes_open_start is None:
                    eyes_open_start = time.time()

                 # Reset only if eyes stay open for 1 second
                if time.time() - eyes_open_start > 1:
                    eyes_closed_start = None
                    CAMERA_STATUS = 0

            # Eyes closed
            else:

                # Reset eye-open timer
                eyes_open_start = None
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

                if eye_elapsed > EYE_SLEEP_TIME:

                    CAMERA_STATUS = 1

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
                else:
                    CAMERA_STATUS = 0
        if CAMERA_STATUS==0:
            status_text="AWAKE"
            status_color=(2,255,0)
        else:
            status_text = "SLEEPING"
            status_color = (0, 0, 255)

            # Show current status
            cv2.putText(
                frame,
                f"STATUS: {CAMERA_STATUS}",
                (10, 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

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

    CAMERA_STATUS = 0
    RUN_CAMERA = False

    print("Camera Stopped")


# Allows standalone testing
if __name__ == "__main__":
    CAMERA()
    
