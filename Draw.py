import cv2
import numpy
import copy
from HandTrackingModule import *

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
cv2.resizeWindow("New Window", 1600, 800)
count = 0
x1 = 0
y1 = 0
path = r"draw.jpg"
blank = numpy.zeros(shape=[512, 512, 3], dtype = "uint8")
blank = cv2.bitwise_not(blank)
newBlank = copy.deepcopy(blank)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With Draw
    # hands = detector.findHands(img, draw=False)  # No Draw
    h = img.shape[0]
    w = img.shape[1]
    blank = cv2.resize(blank, dsize =(w, h), interpolation = cv2.INTER_AREA)
    tipIds = [4, 8, 12, 16, 20]

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right

        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)
        fingers = []
        #length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
        #length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw
        lmList_hand1 = detector.findPosition(img, draw=False)
        
        for id in range(1,5):
                if lmList_hand1[tipIds[id]][2] < lmList_hand1[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        fingerNumCount = 0
        for i in fingers:
            if i == 1:
                fingerNumCount += 1
        
        print('fingernumcount', fingerNumCount)
        if count > 0:
            #print('enters count> 0' )
            #print('count: ', count)
            if (lmList_hand1[tipIds[2]][2] > lmList_hand1[tipIds[1]][2]):
                #print(f'check finger tip indexes-- {tipIds[2]}') # checks to see if tip of index finger is higher than tip of middle finger.
                x2 = lmList_hand1[tipIds[1]][1]                           # a bit buggy - for some reason using the fingers array was even more buggy
                y2 = lmList_hand1[tipIds[1]][2]                           # quick fix should be easy to implement though
                listCoor = [(x1,y1), (x2, y2)]
                if count > 1:
                    print(x2, y2)
                    if 30 <= x2 <= 100 and 30 <= y2 <= 100:
                        print("hello")
                        blank = numpy.zeros(shape=[512, 512, 3], dtype = "uint8")
                        blank = cv2.bitwise_not(blank)
                        blank = cv2.resize(blank, dsize =(w, h), interpolation = cv2.INTER_AREA)
                    
                    if 1210 <= x2 <= 1300 and 20 <= y2 <= 80:
                        from Calculator import *
                        cv2.destroyAllWindows()
                    elif 1210 <= x2 <= 1300 and 120 <= y2 <= 180:
                        from Camera import *
                        cv2.destroyAllWindows()

                    cv2.line(blank, (x1,y1), (x2,y2), (255, 0, 255), thickness = 4)
                    # cv2.line(blank, (x1, y1), (x2, y2), (255, 0, 255), thickness = 4)
                    # cv2.imwrite("draw.jpg",img)
            x1 = lmList_hand1[tipIds[1]][1]
            y1 = lmList_hand1[tipIds[1]][2]
        count += 1

    newImage = cv2.bitwise_and(img, blank)
    newImage = cv2.flip(newImage, 1)
    #different options
    cv2.circle(newImage, (40,50), 30, (0,255,0), cv2.FILLED)
    cv2.putText(newImage, "Calculator", (15, 50), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.30, color=(255,255,255))
    cv2.circle(newImage, (40,120), 30, (0,255,0), cv2.FILLED)
    cv2.putText(newImage, "Camera", (20, 125), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.30, color=(255,255,255))
    
    #Clear button
    cv2.circle(newImage, (1200,50), 30, (255,0,0), cv2.FILLED)
    cv2.imshow("Image", newImage)
    cv2.waitKey(1)
    
    if cv2.waitKey(5) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
