import cv2
import numpy as np

frame_width = 640
frame_height = 480

# Open video capture
cap = cv2.VideoCapture(1)
cap.set(3, frame_width)
cap.set(4, frame_height)

# Create HSV trackbars
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, lambda x: None)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, lambda x: None)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, lambda x: None)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, lambda x: None)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, lambda x: None)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, lambda x: None)

frame_counter = 0

while True:
    frame_counter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_counter = 0

    # Read frame from video capture
    _, img = cap.read()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get trackbar values
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower_range = np.array([h_min, s_min, v_min])
    upper_range = np.array([h_max, s_max, v_max])

    # Create a mask
    mask = cv2.inRange(img_hsv, lower_range, upper_range)

    # Apply the mask to the original image
    result = cv2.bitwise_and(img, img, mask=mask)

    # Convert mask to BGR for horizontal stacking
    mask_colored = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Horizontally stack original image, mask, and result
    h_stack = np.hstack([img, mask_colored, result])

    # Display the horizontally stacked images
    cv2.imshow('Horizontal Stacking', h_stack)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
