import cv2 
from HandTrackingModule import *

# Setup Camera
cap = cv2.VideoCapture(0)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

cv2.resizeWindow("Menu Window", 1600, 800)

#This opens up a splash screen
cv2.imshow("Opening", cv2.imread("Images/OpeningScreen.png"))
cv2.waitKey(3200)
cv2.destroyWindow("Opening")

# cv2.imshow("Opening", cv2.imread("Images/MenuScreen.png"))

#this is the menu
while True:
    # Get Menu Image
    success, img = cap.read()
    img = cv2.flip(img, 1)
    menu = cv2.imread("Images/MenuScreen.png")

    # Find hand and landmarks
    hands, img = detector.findHands(img)  # With Draw

    #circles for buttons
    cv2.circle(img, (250,380), 100, (255,0,0), cv2.FILLED)
    cv2.circle(img, (650,380), 100, (255,0,0), cv2.FILLED)
    cv2.circle(img, (1050,380), 100, (255,0,0), cv2.FILLED)

    #Text
    cv2.putText(img, "Calculator", (170, 390), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color=(255,255,255))
    cv2.putText(img, "Draw", (610, 390), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color=(255,255,255))
    cv2.putText(img, "Camera", (990, 390), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color=(255,255,255))
    
    h = img.shape[0]
    w = img.shape[1]
    tipIds = [4, 8, 12, 16, 20]

    if hands:
        lmList = hands[0]['lmList']
        length,_, img = detector.findDistance(lmList[8], lmList[12], img)
        x, y = lmList[8]

        if length < 50:
            #calculator
            if 150 <= x <= 350 and 280 <= y <= 480:
                from Calculator import *
            #Draw
            elif 550 <= x <= 750 and 280 <= y <= 480:
                from Draw import *
            #Camera
            elif 950 <= x <= 1150 and 280 <= y <= 480:
                from Camera import *

    # cv2.imshow("Menu", menu)
    cv2.imshow("Image", img)

    if cv2.waitKey(5) == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()