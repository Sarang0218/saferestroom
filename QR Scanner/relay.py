import RPi.GPIO as GPIO
import time


relay_pin = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(relay_pin, GPIO.OUT)
while True:
    try:
        """
        print("LOW INPUT")
        GPIO.output(relay_pin, GPIO.LOW)
        time.sleep(0.5)
        """
        print("HIGH INPUT")
        GPIO.output(relay_pin, GPIO.HIGH)
        time.sleep(0.5)
        #print("LOW INPUT")
        #GPIO.output(relay_pin, GPIO.LOW)
        #time.sleep(0.5)
        
        raise KeyboardInterrupt
        
    except KeyboardInterrupt:
        break
    

GPIO.cleanup()