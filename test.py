import cv2
import numpy as np 


img = cv2.imread("과제용 신호등_빨강.jpeg")
print(type(img))
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lower_white=np.array([0,0,150])
upper_white=np.array([179,255,255])

mask=cv2.inRange(hsv,lower_white,upper_white)
# blur=cv2.GaussianBlur(gray,(5,5),0)
kernel=np.ones((5,5),np.uint8)
mask=cv2.erode(mask,kernel)
gray_roi=mask[32:260, 150:210]
color_roi=img[32:260, 150:210]

opening=cv2.dilate(gray_roi,kernel)
output_image=cv2.bitwise_and(color_roi,color_roi,mask=opening)
# cv2.imshow('1',gray_roi)
# cv2.imshow('2',color_roi)
print(type(output_image))
h=output_image.shape[0]
w=output_image.shape[1]
status=True
for i in range(0,h-1):
    for j in range(0,w-1):
        if sum(output_image[i][j])!=0:
            color=(output_image[i][j])
            print(type(color))
            status=False
            break
    if status==False:
        break    
print(color)
if sum(color)==296:
    print('y')
    cv2.putText(img,"YELLOW",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
elif sum(color)==207:
    print('r')
    cv2.putText(img,"RED",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

else:
    print('g')    
    cv2.putText(img,"GREEN",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

# cv2.imshow('3',output_image)
cv2.imshow('main',img)
cv2.waitKey(10000)
cv2.destroyAllWindows()