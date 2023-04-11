// created by youngtose on 03/1/2023 at 7:41pm

// FeatherSense headers
// Include all the files that we need for the built-in sensors
#include <Adafruit_APDS9960.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_LIS3MDL.h>
#include <Adafruit_LSM6DS33.h>
#include <Adafruit_SHT31.h>
#include <Adafruit_Sensor.h>
#include <PDM.h>
#include <LoRa.h>
#include <SPI.h>
#include <RH_RF95.h>

#if defined(ESP8266)
  /* for ESP w/featherwing */ 
  #define RFM95_CS  2    // "E"
  #define RFM95_RST 16   // "D"
  #define RFM95_INT 15   // "B"

#elif defined(ARDUINO_ADAFRUIT_FEATHER_ESP32S2) || defined(ARDUINO_NRF52840_FEATHER) || defined(ARDUINO_NRF52840_FEATHER_SENSE)
  #define RFM95_INT     9  // "A"
  #define RFM95_CS      10  // "B"
  #define RFM95_RST     12  // "C"
#
#endif

// Change to 434.0 or other frequency, must match RX's freq!
#define RF95_FREQ 915.0

// Singleton instance of the radio driver
RH_RF95 rf95(RFM95_CS, RFM95_INT);

int16_t packetnum = 0;  // packet counter, we increment per xmission

// GPS headers
// Include all the files that we need for the GPS featherwing
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

// Particle Sensor headers
#include "Adafruit_PM25AQI.h"

// Create objects for the FeatherSense sensors
Adafruit_BMP280 bmp280;     // temperautre, barometric pressure
Adafruit_SHT31 sht30;       // humidity

// Create objects for the GPS featherwing
SoftwareSerial mySerial(6, 5);
Adafruit_GPS GPS(&mySerial);

// Create objects for the Particle Sensor
// Pin numbers can be changed to match wiring:
SoftwareSerial pmSerial(11, 13);
Adafruit_PM25AQI aqi = Adafruit_PM25AQI();

#define GPSECHO  true

// Create variables for the sensor data 
float temperature, pressure, altitude;
float humidity;
int counter = 0;
short sampleBuffer[256];  // buffer to read samples into, each sample is 16-bits
volatile int samplesRead; // number of samples read
String payload = "";


void setup() {
  Serial.begin(115200);
  delay(5000);

  // initialize the built-in sensors
  bmp280.begin();
  sht30.begin();

  // initialize GPS featherwing
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  GPS.sendCommand(PGCMD_ANTENNA);
  
  // initialize the Particle Sensor
  pmSerial.begin(9600);
  // check that system is connected to master
  if (! aqi.begin_UART(&pmSerial)) {
    while (1) delay(10);
  }
  pinMode(RFM95_RST , OUTPUT);
  digitalWrite(RFM95_RST, HIGH);

  Serial.begin(115200);
  while (!Serial) {
    delay(1);
  }

  delay(100);

  Serial.println("Feather LoRa TX Test!");

  // manual reset
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);

  while (!rf95.init()) {
    Serial.println("LoRa radio init failed");
    Serial.println("Uncomment '#define SERIAL_DEBUG' in RH_RF95.cpp for detailed debug info");
    while (1);
  }
  Serial.println("LoRa radio init OK!");

  // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM
  if (!rf95.setFrequency(RF95_FREQ)) {
    Serial.println("setFrequency failed");
    while (1);
  }
  Serial.print("Set Freq to: "); Serial.println(RF95_FREQ);
  
  // Defaults after init are 434.0MHz, 13dBm, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on

  // The default transmitter power is 13dBm, using PA_BOOST.
  // If you are using RFM95/96/97/98 modules which uses the PA_BOOST transmitter pin, then 
  // you can set transmitter powers from 5 to 23 dBm:
  rf95.setTxPower(23, false);
}

// Get CPU time
uint32_t timer = millis();


void loop(void) {
  temperature = bmp280.readTemperature();
  pressure = bmp280.readPressure();
  altitude = bmp280.readAltitude(1013.25);
  humidity = sht30.readHumidity();

  char c = GPS.read(); 

  PM25_AQI_Data data;
  while (! aqi.read(&data)) {}
  // payload counter
  counter += 1;
  
  // concatenate all data strings to json-like format
  // feathersense
  payload += String("{\"payload\": ") + String(counter) + String(", ");
  payload += String("\"Temp\": ") + String(temperature) + String(", ");
  payload += String("\"Pres\": ") + String(pressure) + String(", ");
  payload += String("\"Alt\": ") + String(altitude) + String(", ");
  payload += String("\"Hum\": ") + String(humidity) + String(", ");
  // gps
  payload += String("\"Speed\": ") + String(GPS.speed) + String(", ");
  payload += String("\"Angle\": ") + String(GPS.angle) + String(", ");
  payload += String("\"Satel\": ") + String(GPS.satellites) + String(", ");
  payload += String("\"Lati\": ") + String(GPS.latitude) + String(", ");
  payload += String("\"Long\": ") + String(GPS.longitude) + String(", ");
  // particle
  payload += String("\"p_gt_03\": ") + String(data.particles_03um) + String(", ");
  payload += String("\"p_gt_05\": ") + String(data.particles_05um) + String(", ");
  payload += String("\"p_gt_10\": ") + String(data.particles_10um) + String(", ");
  payload += String("\"p_gt_25\": ") + String(data.particles_25um) + String(", ");
  payload += String("\"p_gt_50\": ") + String(data.particles_50um) + String(", ");
  payload += String("\"p_gt_100\": ") + String(data.particles_100um) + String("");
  payload += String("}");
  delay(300);

  // Send to LoRa
  delay(1000); // Wait 1 second between transmits, could also 'sleep' here!
  
  // convert string to char array
  const int payload_length = payload.length();
  char* radiopacket = new char[payload_length + 1];
  strcpy(radiopacket, payload.c_str());
  
  // send output to serial port for debugging and tracking
  Serial.println(radiopacket);  
  delay(10);
  
  // Send packet via LoRa
  rf95.send((uint8_t *)radiopacket, payload_length);
  delay(1);
  rf95.waitPacketSent();

  //reset payload
  payload = "";
}
