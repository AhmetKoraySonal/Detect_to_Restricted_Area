import cv2
import numpy as np
import pickle



ix = -1
iy = -1
drawing = False

try:
    with open('ForbiddenArea', 'rb') as f:
        poslist = pickle.load(f)
except:
    poslist = []


def mouseClick(events, x, y, flags, params):
    global ix, iy, drawing, img,poslist

    if events == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y
    elif events == cv2.EVENT_LBUTTONUP:
        if drawing == True:
            poslist.append((ix, iy, x, y))

    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(poslist):
            x1,y1,x2,y2=pos
            if x1<x<x1+(x2-x1) and y1<y<y1+(y2-y1):
                poslist.pop(i)

    with open('ForbiddenArea', 'wb') as f:
        pickle.dump(poslist, f)


#cap=cv2.VideoCapture('C:\\deneme.mp4')

while True:
    img = cv2.imread('C:\\fab.png')
    #sucess,img = cap.read()
    img = cv2.resize(img, (1200, 600))
    for pos in poslist:
        cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+(pos[2]-pos[0]),pos[1]+(pos[3]-pos[1])),(255,0,0),2)
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mouseClick)
    cv2.waitKey(1)
