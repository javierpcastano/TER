import RPi.GPIO as GPIO
import time

motor_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin,GPIO.OUT)
pwm = GPIO.PWM(motor_pin, 800)
pwm.start(0)
# 6 demarre lentement, puis a 26 deraille
speed = 0
increment = 5
try:
    for dc in range(0,round(95/increment)):
        pwm.ChangeDutyCycle(speed)
        speed = speed + increment
        print(f"speed{speed}%")
        time.sleep(3)
except KeyboardInterrupt:
    pass


pwm.stop()
GPIO.cleanup()
