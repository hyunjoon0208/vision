#!/usr/bin/env python

import cv2, time
import numpy as np

cap = cv2.VideoCapture('1.avi')

value_threshold = 60

image_width = 640
scan_width, scan_height = 200, 60
lmid, rmid = scan_width, image_width - scan_width
area_width, area_height = 20, 10
roi_vertical_pos = 380
row_begin = (scan_height - area_height) // 2
row_end = row_begin + area_height
pixel_cnt_threshold = 0.8 * area_width * area_height

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break

    roi = frame[roi_vertical_pos:roi_vertical_pos + scan_height, :]
    cv2.imshow('roi_org',roi)
    frame = cv2.rectangle(frame, (0, roi_vertical_pos),
        (image_width - 1, roi_vertical_pos + scan_height),
        (255, 0, 0), 3)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lbound = np.array([0, 0, value_threshold], dtype=np.uint8)
    ubound = np.array([131, 255, 255], dtype=np.uint8)

    bin = cv2.inRange(hsv, lbound, ubound)
    view = cv2.cvtColor(bin, cv2.COLOR_GRAY2BGR)
    
    left, right = -1, -1

    for l in range(area_width, lmid):
        area = bin[row_begin:row_end, l - area_width:l] 
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            left = l
            break

    for r in range(image_width - area_width, rmid, -1):
        area = bin[row_begin:row_end, r:r + area_width]
        if cv2.countNonZero(area) > pixel_cnt_threshold:
            right = r
            break

    if left != -1:
        lsquare = cv2.rectangle(view,
                                (left - area_width, row_begin),
                                (left, row_end),
                                (0, 255, 0), 3)
    else:
        print("Lost left line")

    if right != -1:
        rsquare = cv2.rectangle(view,
                                (right, row_begin),
                                (right + area_width, row_end),
                                (0, 255, 0), 3)
    else:
        print("Lost right line")



    dst=cv2.Canny(roi,50,200)
    cdst=cv2.cvtColor(dst,cv2.COLOR_GRAY2BGR)
    linesP=cv2.HoughLinesP(dst,1,np.pi/180,50,None,50,10)

    if linesP is not None:
        for i in range(0,len(linesP)):
            l = linesP[i][0]
            cv2.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)


    cv2.imshow("origin", frame)
    cv2.imshow("view", view)
    cv2.imshow('Detected Lines', dst)

    
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
