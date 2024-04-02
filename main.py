import cv2
import cvzone
import pickle
import numpy as np

cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos','rb') as f:
    posList = pickle.load(f)

width, height = 107,47

def checkParkingSpace(imgPro):    # crop image

    spaceCounter = 0

    for pos in posList:
        x,y = pos

        imgCrop = imgPro[y:y+height,x:x+width]
        # cv2.imshow(str(x*y),imgCrop)   # x*y = unique name of each croped imgage
        count = cv2.countNonZero(imgCrop)

        if count <900:
            color = (0,255,0)
            thickness = 5
            spaceCounter+=1
        else:
            color = (0,0,255)
            thickness = 2


        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset=0,colorR=color)

    cvzone.putTextRect(img,f'Free: {spaceCounter}/{len(posList)}',(100,50),scale=3,thickness=5,offset=20,colorR=(0,200,0))


while True:

    # To run video in loop after complete
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        #  CURRENT POSITION                      NO. OF FRAMES IN VIDEO
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    # To convert in grey image
    imgGrey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey,(3,3),1)

    # To convert it in binary   use adaptive threshold
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)

    # USE MEDIAN BLUR TO REMOVE UNNECCESSARY WHITE POINTS IN GREY IMAGE
    imgMedian = cv2.medianBlur(imgThreshold,5)

    # If the lines or values are little bit thin make it thick use dilation
    kernal = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernal,iterations=1)

    checkParkingSpace(imgDilate)

    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)   # To slow video ude 10