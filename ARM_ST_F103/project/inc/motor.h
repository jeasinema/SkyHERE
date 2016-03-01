#ifndef _MOTOR_H_
#define _MOTOR_H_

extern int Target_Speed;
extern float Target_Angle;

void Motor_Init(void);


//用户调用此二函数
void Car_Run(int speed);            //速度闭环
void Car_Turn_Angle(float angle);  //方向定位

//Car_Turn_Angle 的非PID模式调用此函数
void Car_Turn(float angle);   //简单定速顺逆转动

//PID程序调用此二函数
void Car_Turn_Speed(int speed);    //调速转动
void Car_Run_Speed(int speed);     //调速前后运动

int abs(int a);

#endif


