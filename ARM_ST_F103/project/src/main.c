#include "stm32f10x.h"
#include "stm32f10x_tim.h"
#include "delay.h"
#include "encoder.h"
#include "motor.h"
#include "pid.h"
#include "communication.h"
#include "core_cm3.h"
#include <stdio.h>


#define BIT(x)	(1 << (x))
#define speed_fac   1  //由差值计算速度时的系数

int speed;
int turn;
uint8_t fac_us;

int8_t speed_pre=0;
int8_t speed_cur=0;
float angle_tmp=0;

int cmd_speed_pre = 0;
int cmd_angle_pre = 0;


//PID控制的中间变量
int run_output = 0;
int turn_output = 0;

void Speed_Query(void);
void Angle_Query(void);
void SysTick_Init(uint8_t SYSCLK);

int main()
{
	USART3_Config();
	USART2_Config();
	Encoder_Init();
	//while(1);
	Motor_Init();
	SysTick_Init(72);
	Car_Run_Speed(0);
	Car_Turn_Speed(0);   //调用底层函数制动

	// while(!Start_Due)
	// {
	// 	Car_Turn(1);    //方向待定
	// }


	while(1)
	{
		
		//USART1_printf(USART2,"ok\r\n");
		//USART1_printf(USART2,"%d\r\n",TIM2->CCR3);
		//USART_SendData(USART2, TIM3->CNT);
		
		//USART1_printf(USART2,"angle=%d cnt=%d\r\n", (int)Car_Angle,TIM2->CNT);
		//USART1_printf(USART2,"speed=%d cnt=%d\r\n", (int)Car_Speed,TIM3->CNT);
		//USART1_printf(USART2, Cmd_Ble);
		//USART1_printf(USART2,"\r\n");



		//USART1_printf(USART2, "%d-%d-%d-%d-%d-%d-%d-%d\r\n",speed,turn,Car_Speed,(int)Car_Angle,TIM2->CNT,TIM2->CCR3,Motor_Run.PWM,Motor_Turn.PWM);
		
		USART1_printf(USART2, "%d-%d-%d-%d-%d-%d-%d-%d\r\n",speed,turn,Car_Speed,(int)Car_Angle,Motor_Run.PWM,Motor_Turn.PWM,Motor_Run.targetValue,Motor_Turn.targetValue);
		USART1_printf(USART3, "#%d*%d&\r\n", Car_Speed, (int)Car_Angle);
		//USART1_printf(USART2, "ok\r\n");
		//USART_SendData(USART2,USART_ReceiveData(USART2));
		

		cmd_speed_pre = speed;
		cmd_angle_pre = turn;
		sscanf(Cmd_Ble, "#%d-%d*", &speed, &turn);
		if (turn > 180)
		{
			turn = turn % 180;
		}
		else if (turn <= -180)
		{
			turn = turn % -180;
		}

		//USART1_printf(USART3,"aaaa");
		//USART1_printf(USART3, "----%d----", speed);
		//USART_SendData(USART3,turn);  
		if(abs(turn - cmd_angle_pre) != 0)
		{
			Car_Turn_Angle(turn);	
		}
		if(abs(speed - cmd_speed_pre) != 0)
		{
			Car_Run(speed);
		}
		//Car_Turn(1);

	}    
}

void Speed_Query()
{
	speed_pre = speed_cur;
	speed_cur = TIM3 -> CNT;
	if ((speed_cur - speed_pre) < -6000)     //发生上溢
	{
		Car_Speed =  (8000 - speed_pre + speed_cur) >> speed_fac ;   //TIM3的计数值为8000
	}  
	else if ((speed_cur - speed_pre) > 6000)     //发生下溢
	{
		Car_Speed =  (8000 - speed_cur + speed_pre) >> speed_fac ; 
	}
	else
	{
		Car_Speed =  (speed_cur - speed_pre) >> speed_fac ;
	}
}

void Angle_Query()
{
	angle_tmp = TIM2->CNT - zero;
	if(angle_tmp <= 2000)
	{
		Car_Angle = (angle_tmp / 2000) * 180;
	}
	else if(angle_tmp > 2000)
	{
		Car_Angle = ((angle_tmp - 4000) / 2000) * 180;
	}
}

void SysTick_Init(uint8_t SYSCLK)
{
	SysTick->CTRL &=~BIT(2);//选择外部时钟
	SysTick->CTRL |=BIT(1);//打开定时器减到0后的中断请求
	fac_us = SYSCLK/8;//计算好SysTick加载值

	SysTick->LOAD = (u32)fac_us*10000 - 1;//加载时间值   10ms一次
	SysTick->VAL = 1;//随便写个值，清除加载寄存器的值
	SysTick->CTRL |= BIT(0);//SysTick使能
	NVIC_SetPriority(SysTick_IRQn, 0x0);
}


void SysTick_Handler()
{
	
	Speed_Query();
	Angle_Query();
	

	//calcPID(&Motor_Run, Car_Speed);
	calcPID(&Motor_Turn, Car_Angle);
	//Car_Run_Speed(Motor_Run.PWM);
	Car_Turn_Speed(Motor_Turn.PWM);

	//SysTick->VAL = SysTick->LOAD;   //清空VAL，初始化Systick后可有可无
}


