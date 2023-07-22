
import cv2
import numpy as np

# pathResource = "/Users/chaitanyakhandare/Developer/CODE/Python/OpenCV/Resources/lamboCar.png"

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 130)

def empty():
    pass


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)        
        if area > 500:
            cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3)

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            
            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(imgResult, (x,y), (x+w, y+h), (0,255,0), 2)
    return (x+w//2), y


myColors = [[0,179,186,255,46,255]]

myColorValues = [[255,0,0]]
myPoints = []   #[x, y, colorID]

def findColor(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    newPoints = []

    lower = np.array([0, 186, 46])
    upper = np.array([179, 255, 255])
    mask = cv2.inRange(imgHSV, lower, upper)

    x, y = getContours(mask) # we put the masked image in contours
    cv2.circle(imgResult, (x,y), 5, (255,0,0), cv2.FILLED)
    newPoints.append([x,y])
    cv2.imshow("detected", mask)

    return newPoints 


def drawOnCanvas(myPoints, myColorValues):
    for points in myPoints:
        cv2.circle(imgResult, (points[0], points[1]), 5, (255,0,0), cv2.FILLED)
    

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



