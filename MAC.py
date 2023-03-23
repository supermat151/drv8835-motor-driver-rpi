#Libraries
import RPi.GPIO as GPIO
import time
import random
from gpiozero import Motor
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGERright = 8
GPIO_ECHOright = 25

GPIO_TRIGGERmiddle = 15
GPIO_ECHOmiddle = 14

GPIO_TRIGGERleft = 24
GPIO_ECHOleft = 23

#Setting Motors
motorleft = Motor(19, 26)
motorright = Motor(6, 13)
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGERmiddle, GPIO.OUT)
GPIO.setup(GPIO_ECHOmiddle, GPIO.IN)

GPIO.setup(GPIO_TRIGGERright, GPIO.OUT)
GPIO.setup(GPIO_ECHOright, GPIO.IN)

GPIO.setup(GPIO_TRIGGERleft, GPIO.OUT)
GPIO.setup(GPIO_ECHOleft, GPIO.IN)
 
def distanceMid():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERmiddle, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERmiddle, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHOmiddle) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHOmiddle) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distanceLeft():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERleft, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERleft, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHOleft) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHOleft) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distanceRight():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGERright, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGERright, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHOright) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHOmiddle) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:

            motorleft.forward(0.4)
            motorright.forward(0.4)

            distMid = distanceMid()
            print ("MIddle Distance = %.1f cm" % distMid)
            time.sleep(0.01)

            distRight = distanceRight()
            print ("Right Distance = %.1f cm" % distRight)
            time.sleep(0.01)

            distLeft = distanceLeft()
            print ("Left Distance = %.1f cm" % distLeft)
            time.sleep(0.01)

            if distLeft < 15.0:
                motorleft.stop()
                motorright.stop()
                time.sleep(1)

                motorleft.forward(0.35)
                motorright.backward(0.35)
                time.sleep(0.4)
                
                motorleft.stop()
                motorright.stop()
                time.sleep(1)

            elif distRight < 15.0:
                motorleft.stop()
                motorright.stop()
                time.sleep(1)

                motorleft.backward(0.35)
                motorright.forward(0.35)
                time.sleep(0.4)
                
                motorleft.stop()
                motorright.stop()
                time.sleep(1)  

            elif distMid < 25.0:

                X = random.randint(0,1)

                motorleft.stop()
                motorright.stop()
                time.sleep(1)

                motorleft.backward(0.35)
                motorright.backward(0.35)
                time.sleep(0.4)

                #THIS SHIT GO LEFT
                if X == 1:
                    motorleft.stop()
                    motorright.stop()
                    time.sleep(1)

                    motorleft.backward(0.35)
                    motorright.forward(0.35)
                    time.sleep(0.4)

                    motorleft.stop()
                    motorright.stop()
                    time.sleep(1)

                #THIS SHIT GO RIGHT
                else:
                    motorleft.stop()
                    motorright.stop()
                    time.sleep(1)

                    motorleft.forward(0.35)
                    motorright.backward(0.35)
                    time.sleep(0.4)

                    motorleft.stop()
                    motorright.stop()
                    time.sleep(1)
 
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        motorleft.stop()
        motorright.stop()
        GPIO.cleanup()
