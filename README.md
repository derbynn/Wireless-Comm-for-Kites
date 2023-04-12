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
Setting Up an AWS IoT for Raspberry pi connecction
Setting up an AWS IoT account involves creating an AWS account, configuring AWS IoT services, and setting up IoT devices. Here are the steps to get started:

Sign up for an AWS account:
If you don't already have an AWS account, go to https://aws.amazon.com/ and click 'Create an AWS Account'. Follow the instructions to complete the sign-up process.

Sign in to the AWS Management Console:
After creating an AWS account, sign in to the AWS Management Console at https://aws.amazon.com/console/.

Access AWS IoT Core service:
In the AWS Management Console, search for 'IoT Core' in the 'Find Services' search bar or select it from the list of services under the 'Internet of Things' category.

Create a Thing:
a. Click 'Manage' in the left-hand menu, and then click 'Things'.
b. Click 'Create' and then 'Create a single thing'.
c. Enter a name for your IoT device (Thing) and click 'Next'.
d. (Optional) You can add attributes and a Thing type, but for a basic setup, just click 'Create Thing' without adding these.

Create certificates and keys:
a. After creating a Thing, you will be prompted to create certificates and keys. Click 'Create certificate'.
b. Download the public key, private key, and certificate for your Thing.
c. Click 'Activate' to activate the certificate.
d. Click 'Done' to finish the process.

Attach a policy to the certificate:
a. Click 'Secure' in the left-hand menu, and then click 'Policies'.
b. Click 'Create' to create a new policy.
c. Enter a name for the policy and add statements to define permissions. For a basic setup, you can use the following statement to allow all IoT actions:

```
{
   "Effect": "Allow",
   "Action": "iot:*",
   "Resource": "*"
}
```

d. Click 'Create' to save the policy.
e. Go back to the 'Certificates' section under the 'Secure' menu.
f. Find the certificate you created earlier, click the three dots on the right, and select 'Attach policy'.
g. Select the policy you just created and click 'Attach'.

Attach the certificate to the Thing:
a. Go back to the 'Certificates' section under the 'Secure' menu.
b. Find the certificate you created earlier, click the three dots on the right, and select 'Attach thing'.
c. Select the Thing you created and click 'Attach'.

Set up your IoT device:
Configure your IoT device(raspberry pi) to use the AWS IoT endpoint, the downloaded certificate, and private key to connect to AWS IoT Core. 

Test your setup:
After configuring your IoT device, test the connection to AWS IoT Core by subscribing to a topic or publishing messages to a topic. You can use the AWS IoT Core 'Test' feature in the console to monitor messages.
