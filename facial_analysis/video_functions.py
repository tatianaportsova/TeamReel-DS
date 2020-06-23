"""
[?? To do -- fill in ??]
"""

# ----------------------------------------------------------------------------
# Import libraries/modules/functions we will use:

# External (third-party):
import cv2
# import dlib
# from imutils import paths
import numpy as np
import os
# import tensorflow as tf
# from tensorflow import keras

# Internal for our project:


# ----------------------------------------------------------------------------
def get_frames_from_video(video_filename:str):
    """
    Saves all frames from the specified video in subdirectory 'video_frames'.
    """

    # Start capturing the video from the video file:
    # cv2.VideoCapture(0): From first camera or webcam
    # cv2.VideoCapture(1):  From second camera or webcam
    # cv2.VideoCapture("file name.mp4"): From video file
    vid = cv2.VideoCapture(video_filename)

    # Exit if the video capture did not start successfully:
    if not vid.isOpened():
        print("Error: Cannot open video file.")
        exit()

    # Make temp directory 'video_frames' to put the frames in:
    dir_name = 'video_frames'
    if not os.path.exists('video_frames'):
        os.makedirs('video_frames')

    # Get frames:
    current_frame = 0
    total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)

    print(f"Total frames: {total_frames}")
    frame_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Frame width x height: {frame_width} x {frame_height}")
    fps = vid.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second (FPS): {fps}")

    while current_frame <= (total_frames - 1):
        # Get the next frame in the video:
        returned, frame = vid.read()

        if not returned:
            print("Video stream has ended (cannot receive next frame). Exiting.")
            break

        # # Resize the frame:
        # frame = cv2.resize(frame,
        #                   None,
        #                   fx = 0.80,
        #                   fy = 0.80,
        #                   interpolation = cv2.INTER_AREA)

        # # Convert frame from BGR color to grayscale:
        # frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Save frame as image in 'video_frames' directory:
        filename = f"./{dir_name}/frame_{str(current_frame)}.jpg"
        print(f"Creating {filename}")  # [?? To do -- remove ??]
        cv2.imwrite(filename, frame)

        current_frame += 1

    # Release the video capture object & close OpenCV windows:
    vid.release()
    cv2.destroyAllWindows()


# ----------------------------------------------------------------------------
def play_video_file(video_filename:str):
    """
    Plays the specified video file.
    """

    # Start capturing the video from the video file:
    vid = cv2.VideoCapture(video_filename)

    # Exit if the video capture did not start successfully:
    if not vid.isOpened():
        print("Error: Cannot open video file.")
        exit()

    while True:
        # Get the next frame in the video:
        returned, frame = vid.read()

        if not returned:
            print("Video stream has ended (cannot receive next frame). Exiting.")
            break

        # Display the frame:
        cv2.imshow('Frame', frame)

        # Use the "q" key as the quit command:
        # waitKey(0 or <= 0): waits for a key event infinitely
        # waitKey(x:int): waits for a key event for x milliseconds (when x > 0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object & close OpenCV windows:
    vid.release()
    cv2.destroyAllWindows()


# ----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
