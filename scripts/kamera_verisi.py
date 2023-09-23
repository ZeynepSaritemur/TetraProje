#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from basit_uygulamalar.msg import MyImage
from cv_bridge import CvBridge
import cv2
import numpy as np

class RobotKamera():
    def __init__(self):
        rospy.init_node("kamera")
        rospy.Subscriber("camera/rgb/image_raw",MyImage,self.kameraCallback)
        self.bridge = CvBridge()
        rospy.spin()
    
    def kameraCallback(self,mesaj):
        self.foto = self.bridge.imgmsg_to_cv2(mesaj,"bgr8")
        
        # Kırmızı rengi algılamak için alt ve üst eşikleri belirleyin
        lower_red = np.array([0, 0, 100])  # Alt sınır
        upper_red = np.array([100, 100, 255])  # Üst sınır
        
        # Renk filtresini uygulayın
        red_mask = cv2.inRange(self.foto, lower_red, upper_red)
        
        # Gri görüntüyü tersine çevirin (siyah cisim beyaz arkaplan üzerinde olmalı)
        gray = cv2.cvtColor(self.foto, cv2.COLOR_BGR2GRAY)
        
        # Gri görüntüyü tersine çevirin (siyah cisim beyaz arkaplan üzerinde olmalı)
        inverted_gray = cv2.bitwise_not(gray)
        
        # Ters çevrilen görüntüyü eşikleyin (thresholding)
        _, thresh = cv2.threshold(inverted_gray, 128, 255, cv2.THRESH_BINARY)
        
        # Renk maskesini eşiklenmiş görüntü üzerine uygulayın
        masked_thresh = cv2.bitwise_and(thresh, red_mask)
        
        # Siyah cismin konturlarını bulun
        contours, _ = cv2.findContours(masked_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Ağırlık merkezini çizelim
                cv2.circle(self.foto, (cx, cy), 5, (0, 0, 255), -1)
        
        
        cv2.imshow("Robot Kamerasi",self.foto)
        cv2.waitKey(1)
        
nesne = RobotKamera()
        
        
        
        
