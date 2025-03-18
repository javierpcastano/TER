import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)  # This will use I2C bus 1
ads = ADS.ADS1115(i2c)
ads.gain = 1

motor_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin,GPIO.OUT)
pwm = GPIO.PWM(motor_pin, 800)
pwm.start(0)
# 6 demarre lentement, puis a 26 deraille
speed = 0
increment = 5
try:
    while True:
        for dc in range(0,round(100/increment)):
            chan =  AnalogIn(ads , ADS.P0)
            print(f"Raw ADC value: {chan.value}")
            print(f"Voltage: {chan.voltage} V")
            pwm.ChangeDutyCycle(speed)
            speed = speed + increment
            print(f"speed{speed}%")
            time.sleep(3)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()
