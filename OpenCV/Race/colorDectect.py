#
#
#
import cv2
import numpy as np

def FindBigContour(frame, LinelowerRange, LineupperRange):
    colourFilter = cv2.inRange(frame, LinelowerRange, LineupperRange) 

    kernel = np.ones((5,5), np.uint8)
    colourFilter = cv2.dilate(colourFilter, kernel)
    
    Contours, _ = cv2.findContours(colourFilter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return Contours, colourFilter