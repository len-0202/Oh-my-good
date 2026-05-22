import cv2
import time

# Load face detection model

"""
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)
"""

face_cascade = cv2.CascadeClassifier(
    "/home/pbl7/opencv_data/haarcascade_frontalface_default.xml"
)

# Open USB webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Camera resolution
cap.set(3, 640)
cap.set(4, 480)

# Variables
normal_y = None
head_down_start = None

print("Program started")

while True:

    # Read frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to read camera")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # Process detected faces
    for (x, y, w, h) in faces:

        # Draw face rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        # Save normal face position
        if normal_y is None:
            normal_y = y
            print("Normal position saved")

        # Calculate downward movement
        difference = y - normal_y

        # Show difference value
        cv2.putText(
            frame,
            f"Difference: {difference}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Draw sleep detection line LOWER
        threshold = 100

        cv2.line(
            frame,
            (0, normal_y + threshold),
            (640, normal_y + threshold),
            (0, 255, 255),
            2
        )

        # Detect large downward movement
        if difference > threshold:

            # Start timer
            if head_down_start is None:
                head_down_start = time.time()

            elapsed = time.time() - head_down_start

            # Show timer
            cv2.putText(
                frame,
                f"HEAD DOWN {int(elapsed)}s",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            # Sleep condition
            if elapsed > 3:

                cv2.putText(
                    frame,
                    "SLEEP DETECTED",
                    (20, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                print("HEAD_DOWN")

        else:
            # Reset timer
            head_down_start = None

    # Show output window
    cv2.imshow("Head Detection", frame)

    # Exit when pressing q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()