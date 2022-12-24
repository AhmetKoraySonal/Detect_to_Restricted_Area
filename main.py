import cv2
import pickle
import numpy as np
import cvzone

cap=cv2.VideoCapture("C:\\fabrika.mp4")

with open('ForbiddenArea', 'rb') as f:
    poslist = pickle.load(f)





def checkEntery(imgPro):
    global img
    for pos in poslist:
        x1,y1,x2,y2=pos
        cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+(pos[2]-pos[0]),pos[1]+(pos[3]-pos[1])),(255,0,0),2)
        imgCrop=imgPro[y1:y1+(y2-y1),x1:x1+(x2-x1)]
        cv2.imshow(str(x1*y1),imgCrop)

        count=cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x1,y1),scale=2)
        if count>5:
            img=cv2.putText(img,'WARNING',(100,100),cv2.FONT_HERSHEY_DUPLEX,2,
                            (15, 255, 80),5,cv2.LINE_AA)
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success,img=cap.read()
    img=cv2.resize(img,(1200,600))

    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)

    imgMedian=cv2.medianBlur(imgThreshold,5)
    kernel=np.ones((3,3),np.uint8)
    imgDilate=cv2.dilate(imgMedian,kernel,iterations=1)


    checkEntery(imgDilate)

    cv2.imshow("Image",img)
    #cv2.imshow("ImageThreshold",imgThreshold)
    #cv2.imshow("ImageThreshold", imgDilate)
    cv2.waitKey(1)