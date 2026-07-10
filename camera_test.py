import cv2

# Open USB camera (usually index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open USB camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("USB Camera", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
