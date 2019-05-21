import cv2
import numpy as np

def loopVideo(cap, videoName):
    ret, frame = cap.read()
    if ret == False:
        print("Looped")
        cap.release()
        cap = cv2.VideoCapture(videoName)
        ret, frame = cap.read()
    return frame, cap