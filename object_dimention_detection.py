#!/usr/bin/env python3
import cv2
#import numpy as np
from scipy.spatial import distance

cap = cv2.VideoCapture(0)

first_frame = None
euclideanDistanceForOneCm = 21.5

while True:
    
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    cv2.imshow("Frame", frame)
    if first_frame is None:
        first_frame = gray_frame
        continue
  
    difference = cv2.absdiff(first_frame, gray_frame)
    _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
    difference = cv2.dilate(difference, None, iterations=2)
    (_,cnts,_) = cv2.findContours(difference.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) =  cv2.boundingRect(contour)
        
        eu_x1_l = x
        eu_y1_l = y
        eu_x2_l = x+w
        eu_y2_l = y
        
        co_ordinate1_l = (eu_x1_l, eu_y1_l)
        co_ordinate2_l = (eu_x2_l, eu_y2_l)

        euc_dist_length = distance.euclidean(co_ordinate1_l, co_ordinate2_l)
        #print("Eucliden Disance: {}".format(euc_dist_length))
        length_of_obj = euc_dist_length / euclideanDistanceForOneCm
        length_of_obj = round(length_of_obj)
        eu_x1_w = x
        eu_y1_w = y
        eu_x2_w = x
        eu_y2_w = y+h
        
        co_ordinate1_w = (eu_x1_w, eu_y1_w)
        co_ordinate2_w = (eu_x2_w, eu_y2_w)
        
        euc_dist_width = distance.euclidean(co_ordinate1_w, co_ordinate2_w)
        width_of_obj = euc_dist_width / euclideanDistanceForOneCm
        width_of_obj = round(width_of_obj)
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
        print("{} cm x {} cm".format(length_of_obj, width_of_obj))
        cv2.putText(frame,"{} cm x {} cm".format(length_of_obj, width_of_obj), (int((x+w)/2),y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.imshow("Frame", frame)
 
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
