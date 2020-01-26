import RPi.GPIO as GPIO
import time
import random
GPIO.setmode(GPIO.BCM)
PIR_PIN = 21
GPIO.setup(PIR_PIN, GPIO.IN)
def MOTION(PIR_PIN):
    print("Motion Detected!")
    print(random.random())
    print ("PIR Module Test (CTRL+C to exit)")
time.sleep(2)
print ("Ready")

while 1:
    time.sleep(1000)
    try:
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
        print("test")
    except KeyboardInterrupt:
        print (" Quit")
GPIO.cleanup()
