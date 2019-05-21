#
#
#

import cv2
import numpy as np 
from loop import loopVideo
from colorDectect import FindBigContour
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


    LeftContours, LeftcolorFilter = FindBigContour(hsvFrame, LeftLinelowerRange, LeftLineupperRange)
    if LeftContours:
        biggestCont = max(LeftContours, key = cv2.contourArea)
        cv2.drawContours(frame, biggestCont, -1, (255,0,0), 2)
        if cv2.contourArea(biggestCont) > 200:
            M = cv2.moments(biggestCont)
            #calculate x position of centroid
            cX = int(M["m10"] / M["m00"])
            #calculate y position of centroid
            cY = int(M["m01"] / M["m00"])
            #draw a circle at the centroid to show where it is
            #to draw a circle use cv2.circle(image, (x, y), radius, colour, thickness)
            cv2.circle(frame, (cX, cY), 10, (0, 0, 255), -1)       
        
            #we can also draw a line from our car to the centroid and use this line to
            #represent the path we want our car to take
            #to draw a line use cv2.line(image, (x1, y1), (x2, y2), colour, thickness)
            cv2.line(frame, (640, 480), (cX, cY), (255, 0, 255), 5)
        


 
    RightContours, RightcolorFilter = FindBigContour(hsvFrame, RightLinelowerRange, RightLineupperRange)
    if RightContours:
        biggestCont = max(RightContours, key = cv2.contourArea)
        cv2.drawContours(frame, biggestCont, -1, (255,180,0), 2)

  
   
   
    #Display the images we got, these are the original image...(remember to add more)
    cv2.imshow('original image', frame) #display the original frame from video
    cv2.imshow('Left', LeftcolorFilter) #display the original frame from video
    cv2.imshow('Right', RightcolorFilter) #display the original frame from video


    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()