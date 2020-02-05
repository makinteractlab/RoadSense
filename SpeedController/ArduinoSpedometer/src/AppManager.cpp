#include "AppManager.hpp"
#include "ArduinoJson.h"


AppManager::AppManager()
{
    analogWriteResolution(DAC_RESOLUTION);
}


bool AppManager::parseCommand(const String &msg, Stream *const client)
{
    StaticJsonDocument<BUFFER_SIZE> json;
    DeserializationError error = deserializeJson(json, msg);

    // Test if parsing succeeds.
    if (error)
    {
        // Serial.print(F("JSON parse fail"));
        ack (client, "JSON parse fail");
        return false;
    }

    // Parse JSON
    if (json["cmd"] == F("dac")){
        if (!json.containsKey("data")) 
        {
            ack(client,"NoData");
            return false;
        }
        setVoltage (json["data"].as<int>());
        ack(client,"OK"); 
    
    } else {
        ack(client,"Parse Fail");
        return false;
    }

    // all cases left
    return true;
}


void AppManager::ack(Stream *const client,  const String& msg)
{
    if (!client) return;
    String tosend= "{\"ack\":\"" + msg + "\"}\n";
    client->print(tosend);
}

void AppManager::setVoltage(uint16_t milliVolt)
{
    analogWrite(DAC_PIN, map(milliVolt, 0, VOLT_MAX, 0, DAC_MAX));
}

