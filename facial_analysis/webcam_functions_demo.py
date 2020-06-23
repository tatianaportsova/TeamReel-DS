"""
[?? To add ??]
"""





# importing the necessary libraries
import cv2
import numpy as np

# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


# Loop untill the end of the video
while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0,
    #                      interpolation = cv2.INTER_CUBIC)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # conversion of BGR to grayscale is necessary to apply this operation
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # define q as the exit button
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()
