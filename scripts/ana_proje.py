#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from basit_uygulamalar.msg import MyImage, Lazer
from cv_bridge import CvBridge
import cv2
import numpy as np
from basit_uygulamalar.msg import Hiz


class RobotKamera():
    def __init__(self):
        rospy.init_node("kamera")
        rospy.Subscriber("camera/rgb/image_raw", MyImage, self.kameraCallback)
        self.pub = rospy.Publisher("cmd_vel",Hiz,queue_size = 10)
        self.Hiz_mesaji = Hiz()
        self.bridge = CvBridge()
        rospy.spin()
        rospy.init_node("Lazer_verisi")
        self.pub=rospy.Publisher("Cmd_Value",Hiz ,queue_size=10)
        self.hiz_mesaji = Hiz()
        rospy.Subscriber("scan", Lazer,self.laserCallback)
    def lazerCallback(self,mesaj):
        sol_on = list(mesaj.ranges[0:9])
        sag_on = list(mesaj.ranges[350:359])
        on = sol_on + sag_on
        sol = list(mesaj.ranges[80:100])
        sag = list(mesaj.ranges[260:280])
        arka = list(mesaj.ranges[170:190])
        min_on = min(on)
        min_sol = min(sol)
        min_sag = min(sag)
        min_arka = min(arka)
        print(min_on,min_sol,min_sag,min_arka)
        if min_on < 1.0:
            self.hiz_mesaji.linear.x=0.0
            self.hiz_mesaji.linear.y=0.0
            self.hiz_mesaji.angular.z=0.0
    def kameraCallback(self, mesaj):
        self.cap = self.bridge.imgmsg_to_cv2(mesaj, "bgr8") #image mesajını bir opencv 'cv::Mat tipine dönüştürmek için.
        
        #kırmızı alanı bulmak için
        lower_red = np.array([0,50,50]) 
        upper_red = np.array([10,255,255])
        
        hsv = cv2.cvtColor(self.cap, cv2.COLOR_BGR2HSV)
    
        mask = cv2.inRange(hsv, lower_red, upper_red)
        mask = cv2.erode(mask, (5, 5), iterations=9)
        mask = cv2.medianBlur(mask, 7)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (5, 5))
        mask = cv2.dilate(mask, (5, 5), iterations=1)

        _, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    
        cnts,_ = cv2.findContours(thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        frame_merkez_x = self.cap.shape[1]/2
        frame_merkez_y = self.cap.shape[0]/2

        if len(cnts) > 0:
          c = max(cnts, key=cv2.contourArea)
          ((x, y), radius) = cv2.minEnclosingCircle(c)

          
          cv2.line(self.cap, (int(frame_merkez_x),int(frame_merkez_y)),(int(x),int(y)),(0,0,0),3)

          hata_x = int(x) - int(frame_merkez_x)
          
          #hiz alma ve takip etme için:
            
          self.Hiz_mesaji.linear.x = 0.5 # ileri gitmesi icin
          self.Hiz_mesaji.angular.z = -hata_x/100
          self.pub.publish(self.Hiz_mesaji)
          if radius > 150:
              self.Hiz_mesaji.linear.x = 0.0
              self.Hiz_mesaji.angular.z = 0.0
              self.pub.publish(self.Hiz_mesaji) 

        else:
            #self.Hiz_mesaji.linear.x = 0.0
            self.Hiz_mesaji.angular.z = 0.5
            self.pub.publish(self.Hiz_mesaji)
        cv2.imshow("kamera", self.cap)
        cv2.waitKey(1)

RobotKamera()
