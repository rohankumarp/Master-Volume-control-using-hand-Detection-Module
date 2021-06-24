import cv2
import mediapipe as mp
import time



class Detector():
    def __init__(self ,mode = False,maxhands= 2 , detectconfidence=0.5,trackconfidence=0.5 ):
        self.mode = mode
        self.maxhands=maxhands
        self.detectconfidence=detectconfidence
        self.trackconfidence=trackconfidence


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode , self.maxhands , self.detectconfidence, self.trackconfidence)
        self.mpDraw = mp.solutions.drawing_utils      # to draw the points and lines on hands

    def FindHands(self,img,draw=True) :
        imgrbg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgrbg)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:   # if there are many hands then.....
            for handlmrk in self.result.multi_hand_landmarks: # for each hand do the following....
                #only if we want to draw landmarks if we dont want to draw we can provide false for the parameter draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handlmrk, self.mpHands.HAND_CONNECTIONS)
        return img



    def findPosition(self, img, numHands=0, draw=True):

         lmList=[]

         if self.result.multi_hand_landmarks:
             myHand=self.result.multi_hand_landmarks[numHands]


             for id, lm in enumerate(myHand.landmark):
                  h, w, c = img.shape  # c means channels that is the color components
                  cx, cy = int(lm.x * w), int(lm.y * h)
                  #print(id, cx, cy)
                  lmList.append([id , cx  ,cy])
                  if draw:
                      cv2.circle(img, (cx, cy), 3, (255, 0, 255), 5, cv2.FILLED)
         return lmList



def main() :
    # for fps
    pTime = 0  # previous time
    cTime = 0  # current time
    cap = cv2.VideoCapture(0) #Captures the live video
    detector=Detector() # this is an instance of class Detector

    while True:
        ret, img = cap.read()  # ret returns if the image is present or not
        img=detector.FindHands(img)  # to find hands we are calling the FindHands method
        lmList=detector.findPosition(img,draw=False)
        if len(lmList) !=0 :
            print(lmList[4])

        # to find the fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # to display the text on screen
        cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1.6, (0, 255, 255), 2)

        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()







if __name__ ==  '__main__' :
    main()