#ifndef __APP_MANAGER__H__
#define __APP_MANAGER__H__


#include <Arduino.h>
#include "constants.hpp"

enum WAVE {SQUARE_WAVE, SIN_WAVE, TRIANGLE_WAVE, SAW_WAVE};
typedef void (*TimerCallback)();


class AppManager
{
    public:
        inline static AppManager& getInstance()
        {
            static AppManager instance;
            return instance;
        }
       
        bool parseCommand (const String& msg, Stream* const client);
       
        // DAC
        void setVoltage (uint16_t milliVolt);


    private:
       
        void ack (Stream* const client, const String& msg);
       
        AppManager();  
        

    public:
        // Do not implement
        AppManager(AppManager const&)      = delete;
        void operator=(AppManager const&)  = delete;
};


#endif