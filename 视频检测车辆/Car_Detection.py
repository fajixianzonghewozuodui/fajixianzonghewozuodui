import cv2
import numpy as np

car_cascade = cv2.CascadeClassifier('cars.xml')
cap = cv2.VideoCapture('video1.avi')
while(cap.isOpened()):
    ret, image = cap.read()
    cv2.waitKey(20)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray,1.1,1)
    for(x,y,w,h) in cars:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imshow('cars',image)
    if cv2.waitKey(30) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break