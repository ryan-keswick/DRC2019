#
#
#

import serial
import cv2
import numpy as np 
from loop import loopVideo
from colorDectect import FindBigContour
from output import output_speed, output_steering
import heapq
import time
ver = "Ver 1.0.9v now changes sat!!"
print(ver)
time.sleep(2)

#Ard
port = "/dev/ttyACM0"
ard = serial.Serial(port, 9600, timeout=5)

start = time.time()

middlePix = 320
yPix = 480
delay = 0
lap = 0
#*******************Adjust these values***********************************************
LeftLinehLower = 93
LeftLinesLower = 20
LeftLinevLower = 35 
LeftLinehUpper = 116 
LeftLinesUpper = 221 
LeftLinevUpper = 114 
#Put these values into an array, this will be helpful when passing it to functions later
LeftLinelowerRange = (LeftLinehLower, LeftLinesLower, LeftLinevLower)
LeftLineupperRange = (LeftLinehUpper, LeftLinesUpper, LeftLinevUpper)
#*************************************************************************************
RightLinehLower = 22
RightLinesLower = 81 
RightLinevLower = 99 
RightLinehUpper = 27  
RightLinesUpper = 248  
RightLinevUpper = 181 
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
FinishLinehLower = 48 
FinishLinesLower = 36
FinishLinevLower = 144 
FinishLinehUpper = 69 
FinishLinesUpper = 63 
FinishLinevUpper = 162 
#Put these values into an array, this will be helpful when passing it to functions later
FinishLinelowerRange = (FinishLinehLower, FinishLinesLower, FinishLinevLower)
FinishLineupperRange = (FinishLinehUpper, FinishLinesUpper, FinishLinevUpper)

# Used for Prerecored Vid`
'''
input_vid = "TrackTest4.avi" 
video = cv2.VideoCapture(input_vid)
if video.isOpened() is False:
    print("Error opening video file")
    '''
# Used for webcam
cap = cv2.VideoCapture(0)
RcX = 0
LcX = 0
frameskip = 0
frameski = 0
frames = 0

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

print(str(output_speed(10)))
ard.write(str.encode((output_speed(10))))

while True:
    # Used for webcam
    ret, frame = cap.read()
    
    #The first thing we want to do is read in a frame from the video
    # This is used for looping a prerecorded vid
   # frame, video = loopVideo(video, input_vid)
  
    # Small Blur to Make Masking More Consistent
    blur = cv2.GaussianBlur(frame, (3,3), 0)

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)


    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    ####
    frame[...,1] = frame[...,1] * 1.4

    frame[...,2] = frame[...,2]* 0.6
    ####


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
        cv2.drawContours(frame, biggestCont, -1, (8,255,255), 2)
        if cv2.contourArea(biggestCont) > 200:
            R = cv2.moments(biggestCont)
            #calculate x position of centroid
            RcX = int(R["m10"] / R["m00"])
            #calculate y position of centroid
            RcY = int(R["m01"] / R["m00"])
            #draw a circle at the centroid to show where it is
            cv2.circle(frame, (RcX, RcY), 10, (0, 255, 255), -1)       
            cv2.line(frame, (middlePix, yPix), (RcX, RcY), (0, 255, 255), 5)


    ObstacleContours, ObstaclecolorFilter = FindBigContour(hsvFrame, ObstacleLinelowerRange, ObstacleLineupperRange)
    if ObstacleContours:
        BigContours = heapq.nlargest(3, ObstacleContours, key=cv2.contourArea)
        for contour in BigContours:
            if cv2.contourArea(contour) > 200:
                cv2.drawContours(frame, contour, -1, (255,180,180), 2)
                O = cv2.moments(contour)
                #calculate x position of centroid
                OcX = int(O["m10"] / O["m00"])
                #calculate y position of centroid
                OcY = int(O["m01"] / O["m00"])
                #draw a circle at the centroid to show where it is
                cv2.circle(frame, (OcX, OcY), 10, (0, 0, 255), -1)       


    #  Direction calculation
    Rdist = abs(middlePix - RcX)
    Ldist = abs(middlePix - LcX)
    cv2.circle(frame, (Rdist-Ldist+middlePix, int(yPix/2)),10,  (0,0,255), -1)

    #Slowing down output
    if frameskip is 6:
        frameskip = 0
        # diff is the steering
        diff = Rdist - Ldist
        # Speed is how fast the car should go
        speed = abs(-0.0006*diff*diff+100)
        print(str(output_steering(diff)))
        ard.write(str.encode((output_steering(diff))))
# Prints the speed once at the start so this isn't nessacary 
    if frameski is 24: 
        frameski = 0
        print(str(output_speed(10)))
        ard.write((str.encode(output_speed(10))))

    # Lap detection
    delay = delay + 1
    FinishContours, _ = FindBigContour(hsvFrame, FinishLinelowerRange, FinishLineupperRange)
    cv2.putText(frame, "Lap " + str(lap), (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,90,255), 2, cv2.LINE_AA)
    # When the finish line is detected set delay to zero and count the lap
    if FinishContours:
        contour = max(FinishContours, key=cv2.contourArea)
        cv2.drawContours(frame, contour,-1, (0,0,0), 2)
        #print(str(delay) + ' '+ str(cv2.contourArea(contour)))
        if delay > 100:
            if cv2.contourArea(contour) > 5000:
                lap = lap + 1
                delay = 0

    cv2.putText(frame, str(ver), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,90,255), 2, cv2.LINE_AA)
    frameskip = frameskip + 1
    frameski = frameski + 1
    #Display the images we got, these are the original image...(remember to add more)
    cv2.imshow('original image', frame) #display the original frame from video
    cv2.imshow('Left', LeftcolorFilter) #display the original frame from video
    cv2.imshow('Right', RightcolorFilter) #display the original frame from video
    cv2.imshow('Ofpsbstacles', ObstaclecolorFilter)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    frames = frames + 1

    if ret == True:
        out.write(frame)

end = time.time()
secs = end - start
fps = frames/secs

out.release()
cap.release()
print("Frames: " + str(fps))
video.release()
cv2.destroyAllWindows()
