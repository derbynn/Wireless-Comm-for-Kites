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
#### Setting Up an AWS IoT for Raspberry pi connection
Setting up an AWS IoT account involves creating an AWS account, configuring AWS IoT services, and setting up IoT devices. Here are the steps to get started:

#### Sign up for an AWS account:
If you don't already have an AWS account, go to https://aws.amazon.com/ and click 'Create an AWS Account'. Follow the instructions to complete the sign-up process.

#### Sign in to the AWS Management Console:
After creating an AWS account, sign in to the AWS Management Console at https://aws.amazon.com/console/.

There are 2 options for signing into AWS Management Console with distinct access levels and privileges: the root user and IAM (Identity and Access Management) users
1. **Root user**: The original account owner with full access to all AWS resources and services. Should be used sparingly and only for essential tasks such as  such as account billing management, changing the account's email address.
2. **IAM user**: Created within an AWS account and can be assigned specific permissions to manage AWS resources. Should be used for everyday tasks and applications as a good security practice.

#### Access AWS IoT Core service:
In the AWS Management Console, search for 'IoT Core' in the 'Find Services' search bar or select it from the list of services under the 'Internet of Things' category.

#### Create a Thing (a "thing" is a representation of a physical device or logical entity that you can connect to the AWS IoT platform. A thing can be any device that sends and receives data, such as sensors, microcontrollers, smartphones,etc):
1. Click 'Manage' in the left-hand menu, and then click 'Things'.
2. Click 'Create things' and then 'Create a single thing'.
3. Enter a name for your IoT device (Thing) and click 'Next'.
4. (Optional) Register a certificate for your use case. **Auto-generate a new certificate is recommended by AWS**
5. (Optional) Attach Policies if already created or create a new policy by clicking on 'Create Policy' to create a new policy(follow the policy instructions below)
6. (Optional) You can add attributes and a Thing type, but for a basic setup, just click 'Create Thing' without adding these.

#### Create certificates and keys (if you haven't already auto-generated a new certificate):
1. After creating a Thing, you will be prompted to create certificates and keys. Click 'Create certificate'.
2. Download the public key, private key, and certificate for your Thing.
3. Click 'Activate' to activate the certificate.
4. Click 'Done' to finish the process.

#### Attach a policy to the certificate:
1. Click 'Secure' in the left-hand menu, and then click 'Policies'.
2. Click 'Create' to create a new policy.
3. Enter a name for the policy and add statements to define permissions. For a basic setup, you can use the following statement to allow all IoT actions:

```
{
   "Effect": "Allow",
   "Action": "*",
   "Resource": "*"
}
```

4. Click 'Create' to save the policy.
5. Go back to the 'Certificates' section under the 'Secure' menu.
6. Find the certificate you created earlier, click the three dots on the right, and select 'Attach policy'.
7. Select the policy you just created and click 'Attach'.

#### Attach the certificate to the Thing:
1. Go back to the 'Certificates' section under the 'Secure' menu.
2. Find the certificate you created earlier, click the three dots on the right, and select 'Attach thing'.
3. Select the Thing you created and click 'Attach'.

#### Set up your IoT device:
Configure your IoT device(raspberry pi) to use the AWS IoT endpoint, the downloaded certificate, and private key to connect to AWS IoT Core. 

#### Test your setup:
After configuring your IoT device, test the connection to AWS IoT Core by subscribing to a topic or publishing messages to a topic. You can use the AWS IoT Core 'Test' feature in the console to monitor messages.
