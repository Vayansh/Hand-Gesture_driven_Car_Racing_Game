import math
import cvzone
import cv2 as cv
from ultralytics import YOLO
import numpy as np

model = YOLO('Weights/best.pt')
cap = cv.VideoCapture(0)
className = ['left','right']

while True:
    success, img = cap.read()
    if not success:
        break

    results = model(img,stream= True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 =  box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cvzone.cornerRect(img,(x1,y1,(x2-x1),(y2-y1)),8,colorR=(255,0,0),colorC=(0,255,0))
            cls = className[int(box.cls[0])]
            conf = math.ceil(box.conf[0]*100)/100
            cvzone.putTextRect(img,f'{cls} {conf}',(max(0,x1),max(35,y1-20)),
                               scale=0.8, thickness=1)

    cv.imshow('window',img)
    cv.waitKey(1)

cv.destroyAllWindows()