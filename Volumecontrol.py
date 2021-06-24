import cv2
import time
import numpy as np
import handTrackModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
###################################
width = 640
height = 480


###################################


cap = cv2.VideoCapture(1)
cap.set(3 , width)
cap.set(4 , height)
pTime=0
detect = htm.Detector(detectconfidence=0.8)

# All the volume related part
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()

minvol=volrange[0]
maxvol=volrange[1]
vol=0
volbar=400
volper=0

while True :
    ret , img = cap.read()

    img = detect.FindHands(img)   # this is for detecting hands

    lmlist = detect.findPosition(img , draw=False)   # to find the land marks
    if len(lmlist) !=0 :
        #print(lmlist[4] , lmlist[8])  # to get the positions of tips of thumb and index finger

        tx1 , tx2 = lmlist[4][1] , lmlist[4][2]   #cordinates of tip of thumb
        ix1 , ix2 = lmlist[8][1] , lmlist[8][2]   # cordinates of top of index finger
        lx1,lx2 = (tx1+ix1)//2 , (tx2+ix2)//2     # midpoint of the line

        cv2.circle(img ,(tx1,tx2) , 10 ,(255,0,255) , cv2.FILLED ) # thumb
        cv2.circle(img, (ix1, ix2), 10, (255, 0, 255), cv2.FILLED) #index finger
        cv2.line(img , (tx1,tx2) , (ix1,ix2) , (255,0,255), 3 )    # line
        cv2.circle(img , (lx1,lx2) , 10,(255,0,255) , cv2.FILLED)  # line circle

        length = math.hypot(ix1-tx1 , ix2-tx2)
        #print(int(length))

        # range of length of line is 20 - 230
        # range of volume in pycaw is -65 to 0

        vol = np.interp(length , [20,230] , [minvol , maxvol])
        volbar = np.interp(length , [20,230] , [400 , 150]) # for the bar
        volper = np.interp(length , [20,230] , [0 , 100]) # for the percentage


        #print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 30 :
            cv2.circle(img, (lx1, lx2), 10, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img , (50,150) , (85,400) , (0,255,0), 3)
    cv2.rectangle(img , (50,int(volbar)) , (85,400) , (0,255,0), cv2.FILLED)
    cv2.putText(img,f'{int(volper)} %',(30,450) , cv2.FONT_HERSHEY_COMPLEX , 1 , (4,21,240) , 2 )



    # for the fps part
    cTime = time.time()
    fps=1/(cTime-pTime)
    pTime=cTime


    cv2.putText(img,f'FPS :{int(fps)}',(30,50) , cv2.FONT_HERSHEY_COMPLEX , 1, (255,255,0) , 2 )

    cv2.imshow('image' , img)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break
cv2.destroyAllWindows()
