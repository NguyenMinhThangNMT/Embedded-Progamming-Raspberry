#include <wiringPiI2C.h>
#include <wiringPi.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

int mpu;
#define INT_pin  7

void initMpu(void){
	wiringPiI2CWriteReg8(mpu, 0x19, 9);		//sample rate
	wiringPiI2CWriteReg8(mpu, 0x1A, 0x02);	//DLPF
	wiringPiI2CWriteReg8(mpu, 0x1B, 0x08);	//Gyro
	wiringPiI2CWriteReg8(mpu, 0x1C, 0x10);	//ACC
	wiringPiI2CWriteReg8(mpu, 0x38, 1);		//Interrupt
	wiringPiI2CWriteReg8(mpu, 0x6B, 1);		//CLK source
}

void dataReady(void){
	// clear interrupt flag
	wiringPiI2CReadReg8(mpu, 0x3A);
	// read sensor data
	
}

int main(void){
	// setup i2c interface
	mpu = wiringPiI2CSetup(0x68);
	// check connection
	if(wiringPiI2CReadReg8(mpu, 0x75)!= 0x68){
		printf("Connection fail. \n");
		exit(1);
	}
	// setup operational mode for mpu6050
	initMpu();
	// setup interrupt for INT pin
	pinMode(INT_pin, INPUT);
	wiringPiISR(INT_pin, INT_EDGE_RISING, &dataReady)
	
	return 0;
}