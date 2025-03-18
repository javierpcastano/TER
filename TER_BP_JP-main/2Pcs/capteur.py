import requests
import random
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

server_ip = "http://127.0.0.1:5000/send_data"

#Config du ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
channel = AnalogIn(ads, ADS.P0)


def send_data():
    while True:
        # Données a envoyer
        voltage = channel.voltage 
        timestamp = time.time()
        data_to_send = {"value": 5*voltage, 'timestamp':timestamp}

        try:
            #Envoyer données au serveur
            response = requests.post(server_ip, json=data_to_send)
            print("Sent:" ,data_to_send)
        except Exception as e:
            print(f"Error sending data: {e}")
        time.sleep(1)

if __name__ == "__main__":
    send_data()

