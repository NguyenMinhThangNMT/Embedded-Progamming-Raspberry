//Thay doi do sang led do
#include <wiringPi.h>
#include <stdio.h>
#include <softPwm.h>


//Khai bao chan
#define LEDBLUE 22
#define LEDGREEN 27
#define LEDRED 17
#define BT2 19


//Khai bao bien
int duty=0;
//Tao ham ngat bt2
void ngat_bt2(void){
    if (digitalRead(BT2)==0){

            if(duty<=100)
           {
                duty=duty+25;
            }  
    
        else
           {
             duty=0;
            }
    }
    
}
    


int main(void)

{

    wiringPiSetupGpio();
    
   //khai bao mode
    pinMode(LEDRED, OUTPUT);
    //Khai bao pwm gia tri tu 0 den 100
    softPwmCreate(LEDRED,0,100);
    //Khai bao ngat
    wiringPiISR(BT2,INT_EDGE_FALLING,&ngat_bt2);

    while(1)

    {
      softPwmWrite(LEDRED,duty);
    }
    return(0);
}

