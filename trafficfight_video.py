import cv2
import numpy as np

kernel_size_row = 3
kernel_size_col = 3
kernel = np.ones((3, 3), np.uint8)

cap=cv2.VideoCapture('trafficlight_video.mp4')

red1_lower=np.array([160,230,230])
red1_upper=np.array([180,255,255])

red2_lower=np.array([0,200,240])
red2_upper=np.array([10,255,255])

orange_lower=np.array([15,210,170])
orange_upper=np.array([30,255,255])

green_lower=np.array([60,240,150])
green_upper=np.array([70,255,255])


def find_red(image):
    result=False
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    binary_img=cv2.inRange(hsv,red1_lower,red1_upper)
    binary_img2=cv2.inRange(hsv,red2_lower,red2_upper)

    binary_img=cv2.dilate(binary_img,kernel,iterations=6)

    binary_img2=cv2.dilate(binary_img2,kernel,iterations=6)

    dst=cv2.add(binary_img,binary_img2)
    numOfLabels,labels,stats,centroids = cv2.connectedComponentsWithStats(dst)
    cv2.imshow('dst',dst)
    for i in range(1,numOfLabels):
        # if i<2:
        #     continue
        area=stats[i,cv2.CC_STAT_AREA]
        left=stats[i,cv2.CC_STAT_LEFT]
        top=stats[i,cv2.CC_STAT_TOP]
        width=stats[i,cv2.CC_STAT_WIDTH]
        heigth=stats[i,cv2.CC_STAT_HEIGHT]
        if width*heigth>3000:
            result=True
        
    return result

def find_green(image):
    result=False
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    binary_img=cv2.inRange(hsv,green_lower,green_upper)

    binary_img=cv2.dilate(binary_img,kernel,iterations=6)

    numOfLabels,labels,stats,centroids = cv2.connectedComponentsWithStats(binary_img)
    cv2.imshow('binary',binary_img)
    for i in range(1,numOfLabels):
        # if i<2:
        #     continue
        area=stats[i,cv2.CC_STAT_AREA]
        left=stats[i,cv2.CC_STAT_LEFT]
        top=stats[i,cv2.CC_STAT_TOP]
        width=stats[i,cv2.CC_STAT_WIDTH]
        heigth=stats[i,cv2.CC_STAT_HEIGHT]
        if width*heigth>3000:
            result=True
    return result
    
def find_orange(image):
    result=False
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    binary_img=cv2.inRange(hsv,orange_lower,orange_upper)

    binary_img=cv2.dilate(binary_img,kernel,iterations=6)

    numOfLabels,labels,stats,centroids = cv2.connectedComponentsWithStats(binary_img)
    cv2.imshow('binary2',binary_img)

    for i in range(1,numOfLabels):
        # if i<2:
        #     continue
        area=stats[i,cv2.CC_STAT_AREA]
        # print(cv2.CC_STAT_AREA)
        left=stats[i,cv2.CC_STAT_LEFT]
        top=stats[i,cv2.CC_STAT_TOP]
        width=stats[i,cv2.CC_STAT_WIDTH]
        heigth=stats[i,cv2.CC_STAT_HEIGHT]
        if width*heigth>3000:
            result=True
    return result
    
locations=30,40
while True:
    ret,frame=cap.read()

    if ret:
       red=find_red(frame)
       orange=find_orange(frame)
       green=find_green(frame)

    if red:
        print("RED ON")
        cv2.putText(frame,'RED ON',locations,cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255))
    elif orange:
        print("ORANGE ON")
        cv2.putText(frame,'ORANGE ON',locations,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255))
    elif green:
        print("GREEN ON")
        cv2.putText(frame,'GREED ON',locations,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0))
    else:
        print("nothing")
        cv2.putText(frame,'NOTHING',locations,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0))
    cv2.imshow('frame',frame)

    if cv2.waitKey(33)>0:
        break
cap.release()
cv2.destroyAllWindows()