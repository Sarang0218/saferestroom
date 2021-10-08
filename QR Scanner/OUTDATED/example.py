import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SERVO = 22
GPIO.setup(SERVO, GPIO.OUT)

S = GPIO.PWM(SERVO, 50)
S.start(0)

try:
    while True:
        print("OPEN")
        S.ChangeDutyCycle(2.5)
        time.sleep(1)
        print("CLOSE")
        S.ChangeDutyCycle(9.8)
        time.sleep(1)
except KeyboardInterrupt:
    S.stop()

GPIO.cleanup()