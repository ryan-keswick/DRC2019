#
#
#

import cv2
import numpy as np 
from loop import loopVideo

input_vid = "ObstacleTest1.av1"
video = cv2.VideoCapture(input_vid)

if video.isOpened() is False:
    print("Error opening video file")

#*******************Adjust these values***********************************************
LeftLinehLower = 106
LeftLinesLower = 32
LeftLinevLower = 134
LeftLinehUpper = 109
LeftLinesUpper = 161
LeftLinevUpper = 204
#Put these values into an array, this will be helpful when passing it to functions later
LeftLinelowerRange = (LeftLinehLower, LeftLinesLower, LeftLinevLower)
LeftLineupperRange = (LeftLinehUpper, LeftLinesUpper, LeftLinevUpper)
#*************************************************************************************
RightLinehLower = 23 
RightLinesLower = 67
RightLinevLower = 152
RightLinehUpper = 28
RightLinesUpper = 192
RightLinevUpper = 200
#Put these values into an array, this will be helpful when passing it to functions later
RightLinelowerRange = (RightLinehLower, RightLinesLower, RightLinevLower)
RightLineupperRange = (RightLinehUpper, RightLinesUpper, RightLinevUpper)
#*************************************************************************************


while True:
    #The first thing we want to do is read in a frame from the video
    frame, video = loopVideo(video, "ObstacleTest1.avi")

    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    LeftcolorFilter = cv2.inRange(hsvFrame, LeftLinelowerRange, LeftLineupperRange)
    RightcolorFilter = cv2.inRange(hsvFrame, RightLinelowerRange, RightLineupperRange)

    kernel = np.ones((5, 5), np.uint8)
    LeftcolorFilter = cv2.dilate(LeftcolorFilter, kernel)    #play around with kernel size and operations
    RightcolorFilter = cv2.dilate(RightcolorFilter, kernel)    #play around with kernel size and operations

    # Creates a list of contours points  
    Leftcontours, _ = cv2.findContours(LeftcolorFilter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Rightcontours, _ = cv2.findContours(RightcolorFilter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if Leftcontours:
        biggestCont = max(Leftcontours, key = cv2.contourArea)
        cv2.drawContours(frame, biggestCont, -1, (255,0,0), 2)
   
 
    if Rightcontours:
        biggestCont = max(Rightcontours, key = cv2.contourArea)
        cv2.drawContours(frame, biggestCont, -1, (255,255,50), 2)
   
   
   
    #Display the images we got, these are the original image...(remember to add more)
    cv2.imshow('original image', frame) #display the original frame from video
    cv2.imshow('Left', LeftcolorFilter) #display the original frame from video
    cv2.imshow('Right', RightcolorFilter) #display the original frame from video


    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()