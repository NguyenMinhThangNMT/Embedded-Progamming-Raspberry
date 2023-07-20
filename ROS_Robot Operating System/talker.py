#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64
import RPi.GPIO as GPIO
import time
from gpiozero import Button

import spidev


GPIO.setmode(GPIO.BCM)

# khai boo chan den tin hieu cac muc
muc1 = 26
muc2 = 19
muc3 = 13
led = 33 

# Thiết lập chân GPIO là OUTPUT
GPIO.setup(muc1, GPIO.OUT)
GPIO.setup(muc2, GPIO.OUT)
GPIO.setup(muc3, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)

GPIO.output(muc1, GPIO.HIGH)
GPIO.output(muc2, GPIO.HIGH)
GPIO.output(muc3, GPIO.HIGH)
GPIO.output(led, GPIO.HIGH)

# khia bao cac chan dieu khien
btthang = 17
btlui = 18
bttrai = 22
btphai = 27
btspeed =  14
slowdown = 15

led = 36 

# Thiet lap cho GPIO o muc Cao khi khong nhan
GPIO.setup(btthang, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btlui, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bttrai, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btphai, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btspeed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(slowdown, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# Thiet lap thong so the hien len led 7segment 8digit
spi = spidev.SpiDev()  # Create a SpiDev object
spi.open(0, 0)        # Open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set SPI clock speed to 1 MHz

# Define register addresses for the MAX7219
DIGIT0 = 1
DIGIT1 = 2
DIGIT2 = 3
DIGIT3 = 4
DIGIT4 = 5
DIGIT5 = 6
DIGIT6 = 7
DIGIT7 = 8


# ham gui du lieu den max7219
def send_byte(addr, data):
    spi.xfer2([addr, data])
# Turn on the MAX7219 and set the brightness level
send_byte(0x09, 0xff)   # Decode mode off
send_byte(0x0a, 0x03)   # Intensity 3/16
send_byte(0x0b, 0x07)   # Scan limit 8 digits
send_byte(0x0c, 0x01)   # Power on

chars = {'A': 0b00010000, 'P': 0b11111111, 'B': 0b1111100,'L': 0b0111000, 'R':0b1010000 , 'X':0b1111111}





def thang():
    speed = 0
    a = 0
    #banh trai
    pub2 = rospy.Publisher('/my_diffbot/left_wheel_controller/command', Float64, queue_size=10)
    #banh phai
    pub1 = rospy.Publisher('/my_diffbot/right_wheel_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while GPIO.input(btthang) == GPIO.LOW:
        hello_str = "xe dang chay thang %s" % rospy.get_time()
        rospy.loginfo(hello_str)

        #cai dat toc do cho banh xe
        pub1.publish(speed)
        pub2.publish(-speed)
        print("i =:", speed)

        # kiem tra dieu kien cac de tang toc khac nhau va cac muc toc do toi da khac nhau
        if y == 0 :
            GPIO.output(muc1, GPIO.HIGH)
            GPIO.output(muc2, GPIO.HIGH)
            GPIO.output(muc3, GPIO.HIGH)          
            pub1.publish(0)
            pub2.publish(0)
        elif y == 1:
            speed = speed + 0.03
            if speed > 7:
                speed = 7

        elif y == 2:
            speed = speed + 0.09
            if speed > 11:
                speed = 14

        elif y == 3 :
            speed = speed + 0.15
            if speed > 18:
                speed = 18

  
        # the hien toc do len man hinh
        if speed < 10 :
            e0 = int(speed// 1)
            thapphan = speed - e0
            e1 = (speed -  e0) * 10    
            e2 = int(e1 // 1)
            e3 = int(thapphan*10) % 10 
            send_byte(DIGIT7, e0 )
            send_byte(DIGIT6, e2)
            send_byte(DIGIT5 , e3)
        elif speed >= 10:
            e0 = int(speed// 1)
            thapphan = (speed - e0)*10
            hangchuc = int(e0//10)
            send_byte(DIGIT7, hangchuc )
            soduhangchuc = int(e0 % 10)
            send_byte(DIGIT6, soduhangchuc )
            sosaudaucham = int(thapphan // 1)
            send_byte(DIGIT5, sosaudaucham)

        # Gui trang thai xe di thang gui so 1 
        send_byte(DIGIT3, 1)
        
    #khi tha ga toc do giam dan
    while a  < 100:
        a = a + 1
        time.sleep(0.05)
        speed = speed - 0.3
        if GPIO.input(slowdown) == GPIO.LOW:
            
            speed = speed - 0.7
        else:
            speed = speed - 0.3
        if speed < 0:
            speed = 0
            a = 100
        print("i =:", speed)

        pub1.publish(speed)
        pub2.publish(-speed)
    send_byte(DIGIT3, chars['P'])
  
def lui():
    speed = 0
    a = 0
    pub2 = rospy.Publisher('/my_diffbot/left_wheel_controller/command', Float64, queue_size=10)
    pub1 = rospy.Publisher('/my_diffbot/right_wheel_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while GPIO.input(btlui) == GPIO.LOW:
        pub1.publish(-speed)
        pub2.publish(speed)
        time.sleep(0.005)
        hello_str = "xe dang chay lui %s" % rospy.get_time()
        rospy.loginfo(hello_str)


        # kiem tra dieu kien cac de tang toc khac nhau va cac muc toc do toi da khac nhau
        if y == 0 :
            GPIO.output(muc1, GPIO.HIGH)
            GPIO.output(muc2, GPIO.HIGH)
            GPIO.output(muc3, GPIO.HIGH)  
            pub1.publish(0)
            pub2.publish(0)
        
        elif y == 1:
            speed = speed + 0.03
            if speed > 7:
                speed = 7

        elif y == 2:
            speed = speed + 0.07
            if speed > 14:
                speed = 14

        elif y == 3 :
            speed = speed + 0.1
            if speed > 18:
                speed = 18


        # the hien toc do len man hinh
        if speed < 10:
            e0 = int(speed// 1)
            thapphan = speed - e0
            e1 = (speed -  e0) * 10    
            e2 = int(e1 // 1)
            e3 = int(thapphan*10) % 10 
            send_byte(DIGIT7, e0 )
            send_byte(DIGIT6, e2)
            send_byte(DIGIT5 , e3)
        elif speed >= 10:
            e0 = int(speed// 1)
            thapphan = (speed - e0)*10
            hangchuc = int(e0//10)
            send_byte(DIGIT7, hangchuc )
            soduhangchuc = int(e0 % 10)
            send_byte(DIGIT6, soduhangchuc )
            sosaudaucham = int(thapphan // 1)
            send_byte(DIGIT5, sosaudaucham)
        # gui trang thai xe dang di lui
        send_byte(DIGIT3 , 0)

    while a < 100:
        a = a + 1
        time.sleep(0.05)


        if GPIO.input(slowdown) == GPIO.LOW:
            
            speed = speed - 0.7
        else:
            speed = speed - 0.3


        if speed < 0 :
            speed = 0
            a = 100
        print("i =:", y)       
        pub1.publish(-speed)
        pub2.publish(speed)

    # trang thai xe dung
    send_byte(DIGIT4, chars['P'])
   
def trai():
    speed = 0
    pub2 = rospy.Publisher('/my_diffbot/left_wheel_controller/command', Float64, queue_size=10)
    pub1 = rospy.Publisher('/my_diffbot/right_wheel_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while GPIO.input(bttrai) == GPIO.LOW:
        hello_str = "xe dang re trai %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub1.publish(speed)
        pub2.publish(0)
        speed = speed + 0.07
        time.sleep(0.01)
        if speed > 4 :
            speed = 4

        # gui trang thai xe dang di lui
        send_byte(DIGIT4 , chars['L'])
    pub1.publish(0)
    pub2.publish(0)
    send_byte(DIGIT4 , chars['P'])

def phai():
    speed = 0
    pub2 = rospy.Publisher('/my_diffbot/left_wheel_controller/command', Float64, queue_size=10)
    pub1 = rospy.Publisher('/my_diffbot/right_wheel_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while GPIO.input(btphai) == GPIO.LOW:
        hello_str = "xe dang re phai %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub1.publish(0)
        pub2.publish(-speed)
        speed = speed + 0.07
        time.sleep(0.01)
        if speed > 4 :
            speed = 4
        #send_byte(DIGIT4 , chars['R'])
    pub1.publish(0)
    pub2.publish(0)
    send_byte(DIGIT4 , chars['P'])


    
def xoaytraitaicho():
    pub2 = rospy.Publisher('/my_diffbot/left_wheel_controller/command', Float64, queue_size=10)
    pub1 = rospy.Publisher('/my_diffbot/right_wheel_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while GPIO.input(btphai) == GPIO.LOW and y == 4 :
        hello_str = "xe dang xoay trai tai cho %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub1.publish(-5)
        pub2.publish(5)
    pub1.publish(0)
    pub2.publish(0)






def xoayphaitaicho():
    pub2 = rospy.Publisher('/my_diffbot/left_wheel_controller/command', Float64, queue_size=10)
    pub1 = rospy.Publisher('/my_diffbot/right_wheel_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while GPIO.input(btphai) == GPIO.LOW and y == 4:
        hello_str = "xe dang xoay phai tai cho %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub1.publish(5)
        pub2.publish(-5)
    pub1.publish(0)
    pub2.publish(0)

send_byte(DIGIT0, 0)
y = 0
if __name__ == '__main__':
    try:
        while True:
            # kiem tra dieu kien nut nhan tuong ung voi cac huong duy chuyen
            if GPIO.input(btthang) == GPIO.LOW:
                thang()
            if GPIO.input(btlui) == GPIO.LOW:
                lui()
            if GPIO.input(bttrai) == GPIO.LOW:
                #if y == 4:
                #    xoaytraitaicho()
                #else:
                    trai()
            if GPIO.input(btphai) == GPIO.LOW:
                #if y == 4:
                #    xoayphaitaicho()              
                #else:
                    phai()

            
            # tao cac muc tang toc khac nhau va toc do toi da khac nhau
            if GPIO.input(btspeed) == GPIO.LOW:
                time.sleep(0.02)
                if GPIO.input(btspeed) == GPIO.HIGH:
                                   
                    y = y + 1
                    if y == 1:
                        send_byte(DIGIT0, 1)
                        GPIO.output(muc1, GPIO.LOW)
                        GPIO.output(muc2, GPIO.HIGH)
                        GPIO.output(muc3, GPIO.HIGH)
                        send_byte(DIGIT3, chars['X'])        
                        send_byte(DIGIT2, chars['X']) 
                        send_byte(DIGIT1, chars['X'])         
                    elif y == 2 :
                        send_byte(DIGIT0, 2)
                        GPIO.output(muc1, GPIO.HIGH)
                        GPIO.output(muc2, GPIO.LOW)
                        GPIO.output(muc3, GPIO.HIGH)   
                    elif y  == 3:
                        send_byte(DIGIT0, 3)
                        GPIO.output(muc1, GPIO.HIGH)
                        GPIO.output(muc2, GPIO.HIGH)
                        GPIO.output(muc3, GPIO.LOW)   
 
                    elif y > 3:
                        y = 0

                    if y == 0 :
                        send_byte(DIGIT0, 0)
                        GPIO.output(muc1, GPIO.HIGH)
                        GPIO.output(muc2, GPIO.HIGH)
                        GPIO.output(muc3, GPIO.HIGH)        
            if GPIO.input(slowdown) == GPIO.LOW:
                pass

          
    except rospy.ROSInterruptException:
        spi.close()   




