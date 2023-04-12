# Wireless-Comm-for-Kites

This repository contains code written for the remote, base, and cloud parts of this project.

## Remote Unit

Hardware: Adafruit FeatherSense, PM 2.5 Particle Sensor, Adafruit GPS FeatherWing, Adafruit LoRa FeatherWing\
Code: C++ with compatible Arduino libraries\
Serial port: Enabled (displays sent packets and debugging information)\
Message Latency (rate at which messages are sent) : ~ 1 message per second

## Base Unit

Hardware: Raspberry Pi Zero 2W, LoRa unit\
Code: Python 3 with compatible libraries\
Serial port: Enabled via SSH\
Message Latenncy (rate at which messages are received): 1 message every 3 seconds

## Cloud
Hardware: None\
Code: Query Language for AWS Timestream, other programming langauges can be used\
Serial port: Not Applicable\
Message Latency (rate at which messages are received): variable (depends on network speed)
