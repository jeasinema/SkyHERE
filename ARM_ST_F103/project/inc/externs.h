#ifndef _EXTERNS_H

#define _EXTERNS_H

/*声明全局变量区域，请注明变量来源*/

/*Form delay.h*/
extern u16 fac_ms;
extern u8 fac_us;

/*From timer.h*/
extern u32 Motor1;
extern u32 Motor2;
extern u32 Motor3;

/*From speedcontrol.h*/
extern int RealSpeed[3];

/*From mypid.h*/
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

#endif
