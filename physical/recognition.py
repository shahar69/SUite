import cv2
import imutils
import numpy as np

# Initialize the camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Limit the frame rate
fps = 15
frame_time
int(1000 / fps)

while True:
    # Capture the frame
    ret, frame = camera.read()

    # Resize the frame
    frame = imutils.resize(frame, width=320)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), )

    # Detect edges using Canny
    edged = cv2.Canny(blurred, 30, 150)

    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Hand Recognition", frame)

    # Check for user input to quit the program
    key = cv2.waitKey(frame_time) & 0xFF
    if key == ord("q"):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
