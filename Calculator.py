import cv2
from HandTrackingModule import *
from tkinter import *

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
myEquation = ''
timePassed = 0
timerDelay = 100
timeClicked = 0
validTime = 100

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.w = width
        self.h = height
        self.v = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.w, self.pos[1] + self.h),
                    (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.w, self.pos[1] + self.h),
                    (50, 50, 50), 3)
        cv2.putText(img, self.v, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.w and \
                self.pos[1] < y < self.pos[1] + self.h:
                if timePassed > validTime:
                    cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                                (self.pos[0] + self.w - 3, self.pos[1] + self.h - 3),
                                (255, 255, 255), cv2.FILLED)
                    cv2.putText(img, self.v, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                                5, (0, 0, 0), 5)
                return True
        else:
            return False

class outputBox:
    def __init__(self):
        self.expression = ""
        self.dimensions = (800, 50, 1200, 150)
    
    def draw(self,img):
        x1, y1, x2, y2 = self.dimensions
        cv2.rectangle(img, (x1, y1), (x2,y2),(255, 255, 255), cv2.FILLED)
        cv2.rectangle(img, (x1, y1), (x2,y2), (50, 50, 50), 3)
        if len(self.expression) > 20:
            cv2.putText(img, self.expression[len(self.expression)-21:len(self.expression)-1], (850, 100), cv2.FONT_HERSHEY_PLAIN,
                        2, (50, 50, 50), 2)
        else:
            cv2.putText(img, self.expression, (850, 120), cv2.FONT_HERSHEY_PLAIN,
                        2, (50, 50, 50), 2)

    def changeExpression(self, expression):
        self.expression = expression

buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', 'C', '=']]
buttonList = []

outPutBox = outputBox()

for x in range(4):
    for y in range(4):
        dx = x * 100 + 800
        dy = y * 100 + 150
        # cv2.rectangle(img, (x, dx), (y, dy))
        buttonList.append(Button((dx, dy), 100, 100, buttonListValues[y][x]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)  # With Draw
    for i in buttonList:
        i.draw(img)
    
    outPutBox.draw(img)
    
    if hands:
        lmList = hands[0]['lmList']
        length,_, img = detector.findDistance(lmList[8], lmList[12], img)
        # print (length)
        x, y = lmList[8]

        if length < 50:
            for index, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(index % 4)][int(index / 4)]  # get correct number
                    if myValue == '=':
                        try:
                            myEquation = str(eval(myEquation))
                        except:
                            myEquation = "Error"
                            outPutBox.changeExpression("Error")
                            print("error")
                    elif myValue == "C":
                        myEquation = myEquation[:len(myEquation)-2]
                    else:
                        if myEquation == "Error":
                            myEquation = ""
                        if timePassed >= validTime:
                            timeClicked = timePassed
                            validTime = timeClicked + 800
                            myEquation += myValue
                    outPutBox.changeExpression(myEquation)
                    delayCounter = 1
        

# Show calculator 

        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmarks points
        bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
        centerPoint1 = hand1["center"]  # center of the hand cx,cy
        handType1 = hand1["type"]  # Hand Type Left or Right


        # print(len(lmList1),lmList1)
        # print (lmList1)
        # print(bbox1)
        # print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)
        #length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
        #length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw

        lmList_hand1 = detector.findPosition(img, draw=False)
        tipIds = [4, 8, 12, 16, 20]
        x2 = lmList_hand1[tipIds[1]][1]                           
        y2 = lmList_hand1[tipIds[1]][2] 

        if 10 <= x2 <= 70 and 20 <= y2 <= 80:
            from Draw import *
            cv2.waitKey(1)
            cv2.destroyAllWindows()
        elif 10 <= x2 <= 70 and 120 <= y2 <= 180:
            from Camera import *
            cv2.waitKey(1)
            cv2.destroyAllWindows()


        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmarks points
            bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
            centerPoint2 = hand2["center"]  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type Left or Right

            fingers2 = detector.fingersUp(hand2)
            # print(fingers1, fingers2)
            #length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # with draw
            length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw

    if cv2.waitKey(30) == ord(
                'q'):  # this never triggers which is why I fear this is an infinite loop. Play around with break conditions.
            break  # maybe if the equals symbol is pressed, this break condition is met?
    
    #different options
    cv2.circle(img, (40,50), 30, (0,255,0), cv2.FILLED)
    cv2.putText(img, "Draw", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.30, color=(255,255,255))
    cv2.circle(img, (40,120), 30, (0,255,0), cv2.FILLED)
    cv2.putText(img, "Camera", (20, 125), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.30, color=(255,255,255))
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    timePassed += timerDelay
    print(timePassed, validTime)

cap.release()
cv2.DestroyAllWindows()