#ifndef _MOTOR_H_
#define _MOTOR_H_

extern int Target_Speed;
extern float Target_Angle;

void Motor_Init(void);
void Car_Run(int speed);
void Car_Turn(float angle);   //顺逆转动
void Car_Turn_Angle(float angle);  //方向定位
int abs(int a);

#endif


