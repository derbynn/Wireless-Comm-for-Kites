# Wireless Communication for Kite Based Sensors

This repository contains code written for the remote, base, and cloud parts of this project.

## Features

### Remote Unit

**Hardware**: Adafruit FeatherSense, PM2.5 Air Quality Sensor, Adafruit Ultimate GPS FeatherWing, Adafruit LoRa Radio FeatherWing RFM95x set at 915 MHz\
**Code**: C++ with compatible Arduino libraries\
**Serial port**: Enabled (displays sent packets and debugging information)\
**Message Latency (rate at which messages are sent)**: ~ 1 message per second\
**Indicators**: LEDs\
**Displays**: None

### Base Unit

**Hardware**: Raspberry Pi Zero 2W, LoRa unit\
**Code**: Python 3 with compatible libraries\
**Serial port**: Enabled via SSH\
**Message Latency (rate at which messages are received)**: ~ 1 message every 3 seconds\
**Indicators**: LEDs\
**Displays**: Touchscreen, external display compatible

### Cloud
**Hardware**: None\
**Code**: Query Language for AWS Timestream, other programming langauges can be used\
**Serial port**: Not Applicable\
**Message Latency (rate at which messages are received)**: variable (depends on network speed)\
**Indicators**: Not Applicable\
**Displays**: AWS Grafana Dashboard

## Setup

### Remote Unit

1. Set up the circuit as described in the documentation (coming soon!)
2. Clone the repository
3. In ~/remote, upload the code to the Adafruit FeatherSense via Arduino IDE (much easier than importing packages and other dependencies yourself)
4. Open the serial monitor to view packets and/or debugging messages
5. If only packets can be seen in the serial monitor, everything on the sending end is valid.
6. Check whether the base unit is receiving packets from the remote unit
7. Run tests

### Base Unit

1. Set up the circuit by connecting the power supply and the LoRa unit to the raspberry pi. Make sure the pin assignments in the code match up with the pin connections on the LoRa module and raspberry pi.
2. Clone the repository
3. In ~/base, you can open the shell either on the raspberry pi or through an SSH connection and run the base.py script.
4. Upon establishment of communication with the transmitting LoRa, the LoRa module will initiate reception and concurrently display the incoming packets on the terminal, while simultaneously transmitting it to AWS.

### Cloud

Coming Soon!
