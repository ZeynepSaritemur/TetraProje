# TetraProje

## Projeler
- Eşkenar Üçgen Çizdirme Projesi
- Lidar Verisi ile Nesneyi Algılama Projesi
- Kameradan Obje Tespiti ve Ağırlık Merkezi Bulma Projesi
- Final Projesi

## Eşkenar Üçgen Çizdirme Projesi
### Proje Tanımı
ROS kullanarak turtlebot3 ile kendi mesaj dosyalarımız aracılığıyla robota eşkenar üçgen çizdirmek
### Msg Dosyaları
- Ucgen.msg
```
Vector3 linear
Vector3 angular 
``` 
- Vector3.msg
```
float64 x
float64 y
float64 z
```

## Lidar Verisi ile Nesneyi Algılama Projesi
### Proje Tanımı
ROS kullanarak, turtlebot3 ile kendi mesaj dosyalarımız aracılığıyla robotun önündeki nesneyi algılayıp, nesneye 1 metre kala durmsı
### Msg Dosyaları
- Hiz.msg
```
Vector3 linear
Vector3 angular 
```
- Vector3.msg
```
float64 x
float64 y
float64 z
```
-Lazer.msg
```
std_msgs/Header header
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities
```

## Kameradan Obje Tespiti ve Ağırlık Merkezi Bulma Projesi
### Proje Tanımı 
ROS kullanarak, turtlebot3 ile kendi mesaj dosyalarımız aracılığıyla robotun önündeki kırmızı nesnenin ağırlık merkezini bulup, bunu kamerada göstermesi
### Msg Dosyaları
- MyImage.msg
```
std_msgs/Header header
uint32 height
uint32 width
string encoding
uint8 is_bigendian
uint32 step
uint8[] data
```

## Final Projesi 
### Proje Tanımı 
ROS kullanarak, turtlebot3 ile kendi mesaj dosyalarımız aracılığıyla robotun dunya ortamındaki kırmızı nesneyi algılayana kadar kendi etrafında dönmesi ve kırmızı nesneyi bulduktan sonra belirlenen hızda ona doğru giderken kemaradan ağırlık merkeini göstermesi ve nesnye belli bir mesafe kala durması


