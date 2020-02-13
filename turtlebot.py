#!/usr/bin/python

import cv2,rospy,time
import numpy as numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bridge = CvBridge()
cv_image=np.empty(shape=[0])


def callback(img_data):
    global bridge
    global cv_image
    cv_image = bridge.imgmsg_to_cv2(img_data,"bgr8")

if __name__ == "__main__":
    rospy.init_node("camtest_node")
    rospy.Subscriver("/usb_cam/image_raw", Image,callback)
    time.sleep()
    while not rospy.is_shutdown():
        hsv=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
        cv2.imshow("camera",hsv)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()