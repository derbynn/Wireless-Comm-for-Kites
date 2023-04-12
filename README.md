# Wireless Communication for Kite Based Sensors (MEM 42)

This repository contains code written for the remote, base, and cloud parts of this project.

## Remote Unit

Hardware: Adafruit FeatherSense, PM2.5 Air Quality Sensor, Adafruit Ultimate GPS FeatherWing, Adafruit LoRa Radio FeatherWing RFM95x set at 915 MHz\
Code: C++ with compatible Arduino libraries\
Serial port: Enabled (displays sent packets and debugging information)\
Message Latency (rate at which messages are sent) : ~ 1 message per second\
Indicators: LEDs\
Displays: None

## Base Unit

Hardware: Raspberry Pi Zero 2W, LoRa unit\
Code: Python 3 with compatible libraries\
Serial port: Enabled via SSH\
Message Latenncy (rate at which messages are received): ~ 1 message every 3 seconds
Indicators: LEDs\
Displays: Touchscreen, external display compatible

## Cloud
Hardware: None\
Code: Query Language for AWS Timestream, other programming langauges can be used\
Serial port: Not Applicable\
Message Latency (rate at which messages are received): variable (depends on network speed)\
Displays: AWS Grafana Dashboard
