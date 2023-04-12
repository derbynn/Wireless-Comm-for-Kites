import os
from dotenv import load_dotenv
load_dotenv()

#imports for AWS
import time
import paho.mqtt.client as mqtt
import ssl
import json

#imports specific to the raspberry pi board and LoRa connection
import board
import busio
import digitalio
import adafruit_rfm9x


def on_connect(client, userdata, flags, resultCode):
    print("Connected with result code "+str(resultCode))

def on_publish(client, userdata, mid):
    print("Published data" )

#setup for AWS connection with Raspberry Pi using MQTT protocol
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.tls_set(ca_certs= os.getenv('ca_cert'), certfile=os.getenv('certfile'), keyfile=os.getenv('keyfile'), tls_version= ssl.PROTOCOL_SSLv23 )
client.tls_insecure_set(False)
client.connect("a2ba9zhfcbmwcb-ats.iot.us-east-2.amazonaws.com", 8883, 60) # from REST API endpoint in AWS
client.loop_start()

#setup of the LoRa board for the Raspberry Pi connection, setting the cs and rst pins
cs = digitalio.DigitalInOut(board.D4)
reset = digitalio.DigitalInOut(board.D23)
spi = busio.SPI(board.SCK, MOSI = board.MOSI, MISO = board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
rfm9x.tx_power = 23
rfm9x.spreading_factor = 7


def sendData():
    #packet_count = 0
    while True:    
        try:
	'''
	Packet from LoRa is received and the packet number is removed before finally being sent over to AWS in the proper JSON format.
	Error handling for when no packet is received to show users that no packet was received
	'''
            lora_packet = rfm9x.receive(timeout = 3.0)
            if not lora_packet:
                raise ValueError("No packet received")
            print("Received: {0}".format(lora_packet.decode('latin-1')))
            packet = lora_packet.decode('latin-1')
            payload = json.loads(packet)
            payload_id = payload.pop('payload')
            client.publish("sensorDataTopic", payload=json.dumps(payload), qos=0, retain=False)
        except Exception as ex:
            print("Error: ", ex)
                    
        time.sleep(2)

sendData()

