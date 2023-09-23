#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from basit_uygulamalar.msg import Lazer
from basit_uygulamalar.msg import Hiz

class LazerVerisi():
    def __init__(self):
        rospy.init_node("lazer_verisi") #düğümü bir isim vererek başlatıyoruz
        self.pub = rospy.Publisher("cmd_vel",Hiz,queue_size=10) #hareket için hızı yayınlıyoruz
        self.hiz_mesaji = Hiz()
        rospy.Subscriber("scan",Lazer,self.lazerCallback) #scan konusuna abone olarak lazerCallback'e gidiyoruz
        rospy.spin()
    def lazerCallback(self,mesaj):
        sol_on = list(mesaj.ranges[0:9]) #robotun sol ön kısmındaki engeli algılayıp listeler 
        sag_on = list(mesaj.ranges[350:359]) #robotun sağ ön kısmındaki engeli algılayıp listeler
        on = sol_on + sag_on #sol ön ve sağ önden gelen veriler birleştirilir
        sol = list(mesaj.ranges[80:100]) #robotun sol kısmındaki engeli algılayıp listeler
        sag = list(mesaj.ranges[260:280]) #robotun sağ kısmındaki engeli algılayıp listeler
        arka = list(mesaj.ranges[170:190]) #robotun arka kısmındaki engeli algılayıp listeler
        min_on = min(on) #birden fazla veriden en küçüğünü alır
        min_sol = min(sol)
        min_sag = min(sag)
        min_arka= min(arka)
        print(min_on,min_sol,min_sag,min_arka)
        if min_on < 1.0:
            self.hiz_mesaji.linear.x = 0.0 #robotun engle mesafesi 1 den küçük olduğu an durur
            self.pub.publish(self.hiz_mesaji)
        else: 
            self.hiz_mesaji.linear.x = 0.5 #değilse 0.5 hızla hareketine devam eder
            self.pub.publish(self.hiz_mesaji)
nesne = LazerVerisi()
