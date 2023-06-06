import datetime
from math import cos, sin, asin, sqrt
import math
import re
import adafruit_rfm9x
import digitalio
import busio
import board
import json
import ssl
import paho.mqtt.client as mqtt
import time
import sys
import os
from dotenv import load_dotenv
load_dotenv()
# imports for AWS

# imports specific to the raspberry pi board and LoRa connection


def on_connect(client, userdata, flags, resultCode):
    print("Connected with result code "+str(resultCode))


def on_publish(client, userdata, mid):
    print("Published data")


# setup for AWS connection with Raspberry Pi using MQTT protocol
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.tls_set(ca_certs=os.getenv('ca_cert'), certfile=os.getenv(
    'certfile'), keyfile=os.getenv('keyfile'), tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(False)
client.connect("a2ba9zhfcbmwcb-ats.iot.us-east-2.amazonaws.com",
               8883, 60)  # from REST API endpoint in AWS
client.loop_start()

# setup of the LoRa board for the Raspberry Pi connection, setting the cs and rst pins
cs = digitalio.DigitalInOut(board.D4)
reset = digitalio.DigitalInOut(board.D23)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
rfm9x.tx_power = 23
rfm9x.spreading_factor = 7

# getting time and date for file storage



def get_ground_cordinates():
    lati, long = 0.0, 0.0
    try:
        lora_packet = rfm9x.receive(timeout=3.0)
        if not lora_packet:
            raise ValueError("No packet received")
        print("Received: {0}".format(lora_packet.decode('latin-1')))
        packet = lora_packet.decode('latin-1')
        pack = json.loads(packet)
        lati = pack.pop('lati')
        long = pack.pop('long')
        print(f'Latitude {lati}, Longitude {long}')
        return lati, long
    except Exception as ex:
        print("Error: ", ex)


def lat_long_to_radians(latitude, longitude):
    # convert latitude to radians
    if not latitude or not longitude:
        raise ValueError("Incorrect input for latitude and longitude")

    lateral = latitude.split(',')
    lat_degrees = int(lateral[0][:2])
    lat_minutes = float(lateral[0][2:])
    lat_radians = math.radians(lat_degrees + (lat_minutes / 60))

    # convert longitude to radians
    longit = longitude.split(',')
    long_degrees = int(longit[0][:3])
    long_minutes = float(longit[0][3:])
    long_radians = math.radians(long_degrees + (long_minutes / 60))

    # adjust for negative values
    if lateral[1] == "S":
        lat_radians *= -1
    if longit[1] == "W":
        long_radians *= -1

    return lat_radians, long_radians

global LAT, LONG
LAT, LONG = 0.0, 0.0


def haversine(remote_lat, remote_long):
    """Can be global, defined to separate file"""
    r = 6371.0 
    # LAT, LONG, remote_lat, remote_long = map(radians, [LAT, LONG, remote_lat, remote_long])
    LAT, LONG = lat_long_to_radians(LAT, LONG)
    remote_lat, remote_long = lat_long_to_radians(remote_lat, remote_long)
    lat_dist = remote_lat - LAT
    long_dist = remote_long - LONG
    a = (sin(lat_dist/2) ** 2) + cos(LAT) * \
        cos(remote_lat) * (sin(long_dist/2)**2)
    c = asin(sqrt(a))
    dist = 2 * r * c
    return dist


def get_data_debug():
    while True:
        try:
            lora_packet = rfm9x.receive(timeout=3.0)
            if not lora_packet:
                raise ValueError("No packet received")
            print("Received: {0}".format(lora_packet.decode('latin-1')))

        except Exception as ex:
            print("Error: ", ex)

        except KeyboardInterrupt:
            print("Debug mode deactivated")
            break


def validate_payload(payload):
    #different patterns can be checked for 
    pattern1 = r'^\{"payload": \d+, "Temp": \d+\.\d{2}, "Pres": \d+\.\d{2}, ' \
              r'"Alt": \d+\.\d{2}, "Hum": \d+\.\d{2}, "Spd": \d+\.\d{2}, ' \
              r'"Ang": \d+\.\d{2}, "Satel": \d+\.\d{2}, "Lati": \d+\.\d{2}, ' \
              r'"Long": \d+\.\d{2}, "Fix": \d, "gAlt": \d+\.\d{2}\}$'

    pattern2 = r'^\{"payload": \d+, "Temp": \d+\.\d{2}, "Pres": \d+\.\d{2}, ' \
              r'"Alt": \d+\.\d{2}, "Hum": \d+\.\d{2}\}$'

    if re.match(pattern1, payload) or re.match(pattern2, payload):
        return True
    return False


def sendData():
    #creates a folder for the test results and errors to be stored in
    curr_date = datetime.datetime.now().strftime("%Y-%m-%d")
    test_folder_path = os.path.join("Tests", curr_date)
    error_log_folder_path = os.path.join("Errors", curr_date)
    
    if not os.path.exists(test_folder_path):
        os.makedirs(test_folder_path)

    if not os.path.exists(error_log_folder_path):
        os.makedirs(error_log_folder_path)
    
    formatted_time = datetime.datetime.now().strftime("%H-%M-%S")
    packet_file = formatted_time+'.txt'

    while True:
        try:
            #Packet from LoRa is received and the packet number is removed before finally being sent over to AWS in the proper JSON format.
            lora_packet = rfm9x.receive(timeout=1.0)
            if not lora_packet:
                raise ValueError("No packet received")
            packet = lora_packet.decode('latin-1')
            print("Received: {0}".format(packet))
            payload = json.loads(packet)
            if validate_payload(payload):
            #write the packet to the test log folder

                client.publish("sensorDataTopic", payload=json.dumps(
                    payload), qos=0, retain=False) 
                with open(packet_file, 'a') as file:
                    file.write(json.dumps(payload)+ '\n')
                new_file_path = os.path.join(test_folder_path, os.path.basename(packet_file))
                os.rename(packet_file, new_file_path)
            #write the error/unvalidated file to the error log folder
            else:
                with open(packet_file, 'a') as file:
                    file.write(json.dumps(payload)+ '\n')
                new_file_path = os.path.join(error_log_folder_path, os.path.basename(packet_file))
                os.rename(packet_file, new_file_path)
        #Error handling for when criteria is not matched
        except Exception as ex:
            print("Error: ", ex)
        except KeyboardInterrupt:
            print("The program has been terminated")
            break


def menu():
    menu = '''Enter the command you want to execute. 
1. Send the receiving data to AWS
2. Show the data without sending
3. Setup GPS cordinates for base unit with the remote unit
Press x to exit ;)
            '''
    print(menu)


if __name__ == "__main__":
    command = input(menu())
    while True:
        if command == 1:
            sendData()
            command = input(menu()) 
        elif command == 2:
            get_data_debug()
            command = input(menu())
        elif command == 3:
            LAT, LONG = get_ground_cordinates()
            command = input(menu())
        elif command == 'x':
            break
        else:
            menu()


