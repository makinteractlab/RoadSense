#include <Arduino.h>
#include "constants.hpp"
#include "AppManager.hpp"
#include "ArduinoJson.h"


// FORWARD DECLARATIONS
void onMessageReady (const String& msg, Stream* const client);
void setVoltage(uint16_t milliVolt);

// GLOBALS

String buffer ="";
StaticJsonDocument<BUFFER_SIZE> json;


void setup()
{
  Serial.begin(BAUD_RATE);
  Serial.println("Ready");
  AppManager::getInstance().setVoltage(0);
}

void loop()
{
  // Serial
  while (Serial.available())
  {
    char inChar = (char)Serial.read();
    if (inChar == '\n')
    {
      onMessageReady(buffer, &Serial);
      buffer = "";
    }
    else
    {
      buffer += inChar;
    }
  }
}


void onMessageReady (const String& msg, Stream* const client)
{
  if (!client) return;
  bool ack= AppManager::getInstance().parseCommand(msg, client);
  if (!ack) buffer ="";
}




