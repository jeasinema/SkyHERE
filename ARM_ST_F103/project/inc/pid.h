#ifndef __PID_H
#define __PID_H

#include "stm32f10x.h"

typedef struct 
{
		const int ID;
        int targetValue;
        float Kp;
        float Ki;
        float Kd;
        float integrationError;
        int lastError;
		int PWM;
}PID;

extern PID Motor_Run, Motor_Turn;  //传参时注意应当取地址
void calcPID(PID *pid, int input);

#endif
