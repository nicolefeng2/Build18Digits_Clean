from HandTrackingModule import *

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=4) # maybe change maxHands to 2

#previousTime
pTime = 0

b = False
timePassed = 0
timerDelay = 100
timeClicked = 0
validTime = -100

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # With Draw
    # hands = detector.findHands(img, draw=False)  # No Draw

    tipIds = [4, 8, 12, 16, 20]

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right
        
        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:
            lmList_hand1 = detector.findPosition(img, 1, draw = False)

            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            #Finger Counting code
            if len(lmList_hand1) != 0:
                fingers = []

            fingers2 = detector.fingersUp(hand2)
            length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw

            #centerpoint 1 and centerpoint 2 contain the (x,y) coordinates for each center
            x1,y1 = centerPoint1
            x2,y2 = centerPoint2

        else:
            lmList_hand1 = detector.findPosition(img, 0, draw = False)
            #Finger Counting code
            if len(lmList_hand1) != 0:
                fingers = []

                #Thumb
                if lmList_hand1[tipIds[0]][1] > lmList_hand1[tipIds[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1,5):
                    if lmList_hand1[tipIds[id]][2] < lmList_hand1[tipIds[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                if(fingers[1] == 1):
                    if(fingers[2] == 1):
                        x1 = lmList_hand1[tipIds[1]][1]
                        y1 = lmList_hand1[tipIds[1]][2]
                        if timePassed >= validTime:
                            timeClicked = timePassed
                            validTime = timeClicked + 2500
    if timePassed == validTime:
        cv2.imwrite("cameraCapture.jpg",img)
        break

    #back button
    cv2.rectangle(img, (10,20), (90,40), (0,0,255), -1)

    timePassed += timerDelay
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()


cap.release()
path = r"cameraCapture.jpg"
pic = cv2.imread(path)
cv2.imshow("Picture", pic)
cv2.waitKey(0)
cv2.destroyAllWindows()
