#
#
#

import cv2
import numpy as np 
from loop import loopVideo
from colorDectect import FindBigContour
import heapq

input_vid = "ObstacleTest1.avi"

video = cv2.VideoCapture(input_vid)
middlePix = 640
yPix = 480

if video.isOpened() is False:
    print("Error opening video file")

#*******************Adjust these values***********************************************
LeftLinehLower = 108
LeftLinesLower = 131 
LeftLinevLower = 148
LeftLinehUpper = 111
LeftLinesUpper = 205
LeftLinevUpper = 218
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
ObstacleLinehLower = 157 
ObstacleLinesLower = 78
ObstacleLinevLower = 29 
ObstacleLinehUpper = 175 
ObstacleLinesUpper = 132 
ObstacleLinevUpper = 71 
#Put these values into an array, this will be helpful when passing it to functions later
ObstacleLinelowerRange = (ObstacleLinehLower, ObstacleLinesLower, ObstacleLinevLower)
ObstacleLineupperRange = (ObstacleLinehUpper, ObstacleLinesUpper, ObstacleLinevUpper)
#*************************************************************************************



while True:
    #The first thing we want to do is read in a frame from the video
    frame, video = loopVideo(video, input_vid)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    LeftContours, LeftcolorFilter = FindBigContour(hsvFrame, LeftLinelowerRange, LeftLineupperRange)
    if LeftContours:
        biggestCont = max(LeftContours, key = cv2.contourArea)
        cv2.drawContours(frame, biggestCont, -1, (255,0,0), 2)
        if cv2.contourArea(biggestCont) > 200:
            L = cv2.moments(biggestCont)
            #calculate x position of centroid
            LcX = int(L["m10"] / L["m00"])
            #calculate y position of centroid
            LcY = int(L["m01"] / L["m00"])
            #draw a circle at the centroid to show where it is
            cv2.circle(frame, (LcX, LcY), 10, (0, 0, 255), -1)       
            cv2.line(frame, (middlePix, yPix), (LcX, LcY), (255, 0, 255), 5)
 
    RightContours, RightcolorFilter = FindBigContour(hsvFrame, RightLinelowerRange, RightLineupperRange)
    if RightContours:
        biggestCont = max(RightContours, key = cv2.contourArea)
        cv2.drawContours(frame, biggestCont, -1, (255,180,0), 2)
        if cv2.contourArea(biggestCont) > 200:
            R = cv2.moments(biggestCont)
            #calculate x position of centroid
            RcX = int(R["m10"] / R["m00"])
            #calculate y position of centroid
            RcY = int(R["m01"] / R["m00"])
            #draw a circle at the centroid to show where it is
            cv2.circle(frame, (RcX, RcY), 10, (0, 0, 255), -1)       
            cv2.line(frame, (middlePix, yPix), (RcX, RcY), (255, 0, 255), 5)


    ObstacleContours, ObstaclecolorFilter = FindBigContour(hsvFrame, ObstacleLinelowerRange, ObstacleLineupperRange)
    if ObstacleContours:
        BigContours = heapq.nlargest(3, ObstacleContours, key=cv2.contourArea)
        for contour in BigContours:
            if cv2.contourArea(contour) > 200:
                cv2.drawContours(frame, contour, -1, (255,180,180), 2)
                O = cv2.moments(contour)
                #calculate x position of centroid
                OcX = int(R["m10"] / R["m00"])
                #calculate y position of centroid
                OcY = int(R["m01"] / R["m00"])
                #draw a circle at the centroid to show where it is
                cv2.circle(frame, (OcX, OcY), 10, (0, 0, 255), -1)       



    Rdist = abs(middlePix - RcX)
    Ldist = abs(middlePix - LcX)
    cv2.circle(frame, (Rdist-Ldist+middlePix, int(yPix/2)),10,  (0,0,255), -1)


    print(Rdist - Ldist)
    #Display the images we got, these are the original image...(remember to add more)
    cv2.imshow('original image', frame) #display the original frame from video
    cv2.imshow('Left', LeftcolorFilter) #display the original frame from video
    cv2.imshow('Right', RightcolorFilter) #display the original frame from video
    cv2.imshow('Obstacles', ObstaclecolorFilter)


    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()