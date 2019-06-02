#res
#
#
import cv2
import numpy as np

def FindBigContour(frame, LinelowerRange, LineupperRange):
    colourFilter = cv2.inRange(frame, LinelowerRange, LineupperRange) 

    
    kernel = np.ones((1,1), np.uint8)
    erosion = cv2.erode(colourFilter, kernel, iterations = 1)
    dilation = cv2.dilate(colourFilter, kernel, iterations = 1)
    

    Contours, _ = cv2.findContours(colourFilter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return Contours, colourFilter