# Wireless Communication for Networking Kite-Based Sensors

This repository contains code written for the remote, base, and cloud parts of this project. The project focuses on creating a wireless communication network for kites using LoRa technology to transmit data from remote units to a base unit. The base unit then forwards the data to the cloud for storage and analysis. 

The repository is organized into three main sections: Remote, Base, and Cloud Unit. Each section contains code specific to that component, along with instructions for setup and usage. The Remote Unit code is written in C++ with compatible Arduino libraries, while the Base Unit code is written in Python 3 with compatible libraries. The Cloud section involves querying data stored in AWS Timestream using Timestream Query Language(TQL), a SQL-like language specifically designed for querying time-series data in Timestream, and visualizing the data in AWS Managed Grafana.

## Table of Contents

1. [Features](#features)
   - [Remote Unit](#remote-unit)
   - [Base Unit](#base-unit)
   - [Cloud](#cloud-unit)

2. [Setup](#setup)
   - [Remote Unit](#remote-unit-1)
   - [Base Unit](#base-unit-1)
   - [Cloud Unit](#cloud-unit)
      - [Setting Up an AWS IoT for Raspberry Pi connection](#setting-up-an-aws-iot-for-raspberry-pi-connection)
      - [Setting up AWS Timestream](#setting-up-aws-timestream)

3. [References](#references)

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

### Cloud Unit
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

### Cloud Unit
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
1. Click 'Manage' in the left-hand menu, and then click 'All Devices' and click 'Things'.
2. Click 'Create things' and then 'Create a single thing'.
3. Enter a name for your IoT device (Thing) and click 'Next'.
4. (Optional) Register a certificate for your use case. **Auto-generate a new certificate is recommended by AWS**
5. (Optional) Attach Policies if already created or create a new policy by clicking on 'Create Policy' to create a new policy(follow the policy instructions below)
6. (Optional) You can add attributes and a Thing type, but for a basic setup, just click 'Create Thing' without adding these.

#### Downloading certificates and keys:
1. After creating a Thing, you will be prompted to download certificates and keys.
2. Download the public key, private key, and certificate for your Thing.
3. Click 'Done' to finish the process.

#### Attach a policy to the certificate:
1. Click 'Security' in the left-hand menu, and then click 'Policies'.
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
5. Go back to the 'Certificates' section under the 'Security' menu.
6. Find the certificate you created earlier, click the three dots on the right, and select 'Attach policy'.
7. Select the policy you just created and click 'Attach'.

#### Attach the certificate to the Thing:
1. Go back to the 'Certificates' section under the 'Security' menu.
2. Find the certificate you created earlier, click the three dots on the right, and select 'Attach thing'.
3. Select the Thing you created and click 'Attach'.

#### Set up your IoT device:
Configure your IoT device(raspberry pi) to use the AWS IoT endpoint, the downloaded certificate, and private key to connect to AWS IoT Core. 

#### Test your setup:
After configuring your IoT device, test the connection to AWS IoT Core by subscribing to a topic or publishing messages to a topic. You can use the AWS IoT Core 'Test' feature in the console to monitor messages.

#### Setting up AWS Timestream
AWS Timestream is a time-series database service designed for IoT and operational applications. It provides fast and scalable ingestion and querying of time-series data. To set up AWS Timestream, follow these steps:
1. Sign in to the AWS Management Console:
- Sign in to your AWS account at https://aws.amazon.com/console/. If you don't have an account yet, create one by following the instructions on the website.
2. Create an Amazon Timestream database:
- In the AWS Management Console, navigate to the Amazon Timestream service by typing "Timestream" in the search bar and selecting it from the list of services.
- On the Amazon Timestream home page, click on "Create database".
- Enter a name for your database, choose an optional description, and select a retention policy for your data. The retention policy defines how long your data will be stored in the memory store and magnetic store.
- Click on "Create" to create the database.
3. Create a table:
- In the Timestream console, select the newly created database.
- Click on "Create table".
- Enter a name for your table and select a memory store retention period. Optionally, you can also add tags for your table.
- Click on "Create" to create the table.
4. Documentation for reference: https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html


#### Setting up an AWS IoT Core Rule to ingest data into Timestream:
1. Navigate to the AWS IoT Core console (https://console.aws.amazon.com/iot).
2. In the navigation pane in the left-hand menu, click on "Manage", click on "Message routing", click on "Rules", then click on "Create rule".
3. Enter a name and description(optional) for the rule.
4. In the "Configure SQL statement" section, enter a SQL query to select data from the incoming IoT messages. 
   - For example: **SELECT temperature, humidity FROM 'your/topic’** 
   - ```SELECT <Attribute> FROM <Topic Filter> WHERE <Condition>```
5. In the "Attach rule actions" section, click on "Add action", then select "Timestream table".
6. Choose the Timestream database and table you created earlier. 
   - Add dimensions for your table. 
   -  if your Timestream table has columns Temp and Hum for storing these dimensions, you would map them like this:
      - dimension key: Temp, value: ${Temp}
      - dimension key: Hum, value: ${Hum}
7. Click on "Create role" or select an existing role that allows IoT Core to write to Timestream.
8. On the Review and create page: 
 - Click on "Create" to finalize the rule creation.
9. Connect your IoT devices to AWS IoT Core and start sending data:
    - You need to set up your IoT devices to connect to AWS IoT Core and send data on the MQTT topic specified in your rule query statement. To do this, follow the AWS IoT Core documentation on connecting devices and sending messages: https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-sdk.html
  - Documentation: https://docs.aws.amazon.com/iot/latest/developerguide/iot-rules.html
9. Once you've completed these steps, your IoT devices will send data to AWS IoT Core, which will then ingest the data into Timestream using the rule you've created. You can then query and analyze your time-series data in Timestream.

#### Query your data on Timestream:
Once you have ingested data into your Timestream table, you can query it using the Timestream Query console or the SDKs.
For example, to query data in the Timestream Query console, follow these steps:
- Navigate to the Timestream console.
- Click on the "Query editor" tab.
- Select your database and table from the dropdown menus.
- Write a SQL query to analyze your data (e.g., **SELECT * FROM "MyTimestreamDB"."MyTimestreamTable" LIMIT 100;**).
- Click "Run query."


### References 
[1] A. Industries, "Adafruit Feather NRF52840 sense," adafruit industries blog RSS. [Online]. Available: https://www.adafruit.com/product/4516. [Accessed: Oct. 26, 2022].

[2] "Final Report: Mapping Air Quality with Kite-Based Sensors," EPA, Apr. 16, 2020. [Online]. Available: https://cfpub.epa.gov/ncer_abstracts/index.cfm/fuseaction/display.abstractDetail/abstract_id/10944/report/F. [Accessed: Oct. 26, 2022].

[3] R. Andrews, "Weather Forecast with Meteodrones Weather Drones," Meteomatics, 2021. [Online]. Available: https://www.meteomatics.com/en/meteodrones-weather-drones/.

[4] "Automating Your Home with Grafana and Siemens Controllers," AWS Architecture Blog, Amazon Web Services, Nov. 26, 2019. [Online]. Available: https://aws.amazon.com/blogs/architecture/automating-your-home-with-grafana-and-siemens-controllers/. [Accessed: Mar. 9, 2023].

[5] "Dasaki Ramps 1.4 Enclosure/Box/Case," UltiMaker Thingverse. [Online]. Available: https://www.thingiverse.com/thing:761806. [Accessed: May 9, 2023].

[6] "Magnetic tissue box mount," UltiMaker Thingverse. [Online]. Available: https://www.thingiverse.com/thing:3151805. [Accessed: May 9, 2023].

[7] G. Bland et al., "Aerokats and Rover," NASA/ADS, 2015. [Online]. Available: ui.adsabs.harvard.edu/abs/2015AGUFMED51C0830B/abstract. [Accessed: May 15, 2023].

[8] "Haversine formula in Python (bearing and distance between two GPS points)," Stack Overflow. [Online]. Available: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points. [Accessed: May 15, 2023].

[9] Adafruit Industries, "Adafruit Ultimate GPS FeatherWing Arduino Library," Adafruit Learning System. [Online]. Available: https://learn.adafruit.com/adafruit-ultimate-gps-featherwing/arduino-library. [Accessed: May 15, 2023].

[10] Python Software Foundation, "re - Regular expression operations," Python Documentation. [Online]. Available: https://docs.python.org/3/library/re.html. [Accessed: May 15, 2023].

[11] Google Developers, "Python Regular Expressions," Google Developers. [Online]. Available: https://developers.google.com/edu/python/regular-expressions. [Accessed: May 15, 2023].

[12] Adafruit Industries, "Adafruit Feather Sense Arduino Sensor Example," Adafruit Learning System. [Online]. Available: https://learn.adafruit.com/adafruit-feather-sense/arduino-sensor-example. [Accessed: May 15, 2023].

[13] Adafruit Forums, "GPS Testing and Interpretation," Adafruit Forums. [Online]. Available: https://forums.adafruit.com/viewtopic.php?t=30776. [Accessed: May 15, 2023].

