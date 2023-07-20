//Nhan nut BT1
 //Nhan lan 1 led do sang
 //Nhan lan 2 led xanh la sang
 //Nhan lan 3 led xanh danh sang
 //Nhan lan 4 led r b g nhap nhay
#include <stdio.h>
#include <wiringPi.h>

#define LEDBLUE 17
#define LEDGREEN 27
#define LEDRED 22
#define BT1 26

//Khai bao mot bien dem 
int count =0;

//tao ham interupt cua BT1
void ngat_bt1(void)
{
    
    if (digitalRead(BT1)==0){

            if(count<5)
           {
                count++;
            }  
    
        else
           {
             count=1;
            }
        
    }
}


//Chuong trinh chinh
int main(void)

{
    wiringPiSetupGpio();
    //Set che do Input,OutPut
    
    pinMode(LEDRED,OUTPUT);
    pinMode(LEDGREEN,OUTPUT);
    pinMode(LEDBLUE,OUTPUT);
    pinMode(BT1,INPUT);
    
    
    //thiet lap Interupt wiringPI
    wiringPiISR(BT1,INT_EDGE_FALLING,&ngat_bt1);
    

    while(1)

    {
        //Nhan lan 1 led do sang
        if (count== 1)
        {
        digitalWrite(LEDRED, HIGH);
        digitalWrite(LEDGREEN, LOW);
        digitalWrite(LEDBLUE, LOW);   
        }
        //Nhan lan 2 led xanh la sang
        if (count== 2)
        {
        digitalWrite(LEDRED, LOW);
        digitalWrite(LEDGREEN, HIGH);
        digitalWrite(LEDBLUE, LOW);    
        }
        //Nhan lan 3 led xanh danh sang
        if (count== 3)
        {
        digitalWrite(LEDRED, LOW);
        digitalWrite(LEDGREEN, LOW);
        digitalWrite(LEDBLUE, HIGH); 
        }
        //Nhan lan 4 led r b g nhap nhay
        if (count== 4)
        {
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
        
    }

    return 0;
}
fa
