//BT GPIO led RGB sang nhap nhay lan luot

#include <wiringPi.h>
#include <stdio.h>

//Dinh nghia chan
#define LEDBLUE 14
#define LEDGREEN 15
#define LEDRED 18
#define BT1 26
#define BT2 19



int main(void)

{
  
    wiringPiSetupGpio();
    //khai bao mode
    pinMode(LEDBLUE, OUTPUT);
    pinMode(LEDGREEN, OUTPUT);
    pinMode(LEDRED, OUTPUT);

    while(1)

    {
        //Led do sang
        digitalWrite(LEDRED, HIGH);
        digitalWrite(LEDGREEN, LOW);
        digitalWrite(LEDBLUE, LOW);      
        delay(500);
        //Led xanh la sang
        digitalWrite(LEDRED, LOW);
        digitalWrite(LEDGREEN, HIGH);
        digitalWrite(LEDBLUE, LOW);
        delay(500);
        //Led xanh duong 
        digitalWrite(LEDRED, LOW);
        digitalWrite(LEDGREEN, LOW);
        digitalWrite(LEDBLUE, HIGH);
        delay(500);
  
    }

    return 0;
}

