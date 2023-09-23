#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from basit_uygulamalar.msg import Ucgen
import math

def hareket(pub, cizgisel_hiz, yer_degistirme):
    hareket_hizi = Ucgen()
    hareket_hizi.linear.x = cizgisel_hiz
    guncel_konum = 0
    rate = rospy.Rate(10)  
    

    while guncel_konum < yer_degistirme and not rospy.is_shutdown():
        pub.publish(hareket_hizi)
        rate.sleep()
        guncel_konum += cizgisel_hiz * 0.1 

    # dur 
    hareket_hizi.linear.x = 0
    pub.publish(hareket_hizi)

def dondurme(pub, acisal_hiz, aci):
    hareket_hizi = Ucgen()
    hareket_hizi.angular.z = acisal_hiz
    guncel_aci = 0
    rate = rospy.Rate(10)  
    

    while guncel_aci < aci and not rospy.is_shutdown():
        pub.publish(hareket_hizi)
        rate.sleep()
        guncel_aci += acisal_hiz * 0.1 

    # dur 
    hareket_hizi.angular.z = 0
    pub.publish(hareket_hizi)

def eskenar_ucgen_ciz(pub, side_length):
    cizgisel_hiz = 0.5
    acisal_hiz = 1.0  

    for _ in range(3):
        hareket(pub, cizgisel_hiz, side_length)
        dondurme(pub, acisal_hiz, math.radians(120))

def main():
    rospy.init_node('eskenar_ucgen_cizdirme', anonymous=True)
    pub = rospy.Publisher('/cmd_vel',Ucgen, queue_size=10)

    side_length = 1.0

    eskenar_ucgen_ciz(pub,side_length)


try:
        main()
except rospy.ROSInterruptException:
        pass
