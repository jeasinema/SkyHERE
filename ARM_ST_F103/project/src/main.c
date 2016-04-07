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
#define BOTTOMIMPROVE    //串口通信不畅，直接在底层实现转角的优化

int stop_protect_val = 60;

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

//用于解决170 -> -170问题
int diff_1 = 0;   //原角度
int diff_2 = 0;   //+360
int diff_3 = 0;   //-360

//用于转向优化
int src_1 = 0;   //原位置
int src_2 = 0;   //反向位置
int diff_4 = 0;  //距原位置的角距离
int diff_5 = 0;  //距反向位置的角距离

void Speed_Query(void);
void Angle_Query(void);
void SysTick_Init(uint8_t SYSCLK);

int is_close(int src, int dst);
int speed_reverse_flag = 0;

int main()
{
	USART3_Config();
	USART2_Config();
	Encoder_Init();
	//while(1);
	Motor_Init();
	SysTick_Init(72);
	Car_Run_Speed(0);
	while(!Start_Due)
	{
		Car_Turn_Speed(2000);   //Z向输出标定
	}
	Car_Turn_Angle(0);
	while(1)
	{
		
		//USART1_printf(USART2,"angle=%d cnt=%d\r\n", (int)Car_Angle,TIM2->CNT);
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


		#ifdef BOTTOMIMPROVE  
		// //转向优化
		// if (is_close(Car_Angle,turn))
		// 	turn = turn;
		// else
		// 	turn = turn + 180;
		// 	speed = -speed;
		// if (turn > 180)
		// {
		// 	turn = turn % 180;
		// }
		// else if (turn <= -180)
		// {
		// 	turn = -((-turn) % 180);
		// }

		// Car_Turn_Angle(turn);	
		// Car_Run(speed);
		if (abs(speed) > 0)   //速度为零时不要优化，便于调零
		{
			src_1 = Car_Angle;
		    if (Car_Angle > 0)
		    {
		    	src_2 = -180 + Car_Angle;
		    }
		    else
		    {
		    	src_2 = 180 + Car_Angle;
		    }
		    //calc the angle distance 
		    diff_4 = abs(turn - src_1);   //normal
		    diff_5 = abs(turn - src_2);   //reverse
		    if (diff_4 > 180)
		    {
		    	diff_4 = 360 - diff_4;
		    }
		    if (diff_5 > 180)
		    {
		    	diff_5 = 360 - diff_5;
		    }
		    if (diff_5 >= diff_4)
		   	{
		   		//normal turn
		   	}
		   	else
		   	{
		   		if (turn >=0)
		   		{
		   			turn = -180 + turn;
		   		}
		   		else
		   		{
		   			turn = 180 + turn;
		   		}
		   		speed = -speed; //reverse turn 
		   	}
		}
		#endif


		//解决170 -> -170反转的问题，原理：以170->-170为例，未过180前，turn为190，但是对于calcpid而言，仍然能够正常输出。过了180后，
		//turn就变回-170了，从而恢复正常。
		diff_1 = abs(turn - Car_Angle);
		diff_2 = abs(360 + turn - Car_Angle);
		diff_3 = abs(turn - 360 - Car_Angle);

		if (diff_2 < diff_1)   //+360较小,即170 -> -170
		{
			turn = 360 + turn;
		}
		else if (diff_3 < diff_1)   //-360较小,即-170 -> 170
		{
			turn = turn - 360;
		}
		else
		{
			turn = turn;
		}

		//#ifndef BOTTOMIMPROVE  
		if(abs(turn - cmd_angle_pre) != 0)       //cmd_angle_pre 在读取新值之前被赋值，接下来被赋值的turn又会被更改，因此没有问题
		{
			Car_Turn_Angle(turn);	
		}
		if(abs(speed - cmd_speed_pre) != 0)
		{
			Car_Run(speed);
		}
		stop_protect_val  = (130 - abs(speed)) > 60?60:(130-abs(speed));
		//Car_Turn(1);
		//#endif

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
	angle_tmp = TIM2->CNT - 0;
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
	stop_protect++;
	if (stop_protect > stop_protect_val && speed != 0) {
		memcpy(Cmd_Ble, stop_protect_buff, 20);
	}
	//Speed_Query();
	Angle_Query();

	
    //运动电机仍采用传统控制方式
	//calcPID(&Motor_Run, Car_Speed);
	calcPID(&Motor_Turn, Car_Angle);
	//Car_Run_Speed(Motor_Run.PWM);
	Car_Turn_Speed(Motor_Turn.PWM);   

	//SysTick->VAL = SysTick->LOAD;   //清空VAL，初始化Systick后可有可无
}

int  is_close(int src, int dst)
{
    // if (src < 0)
    //     src = src + 360;
    // if (dst < 0)
    //     dst = dst + 360;
    // //正常情况
    // if (abs(dst - src) <= 90)
    //     return 1;
    // //两种异常
    // else if (dst - src + 360 <= 90)
    //     return 1;
    // else if (src - dst + 360 <= 90)
    //     return 1;
    // else
    //     return 0;
    // src_1 = src;
    // if (src >= 0)
    // {
    // 	src_2 = -180 + src;
    // }
    // else
    // {
    // 	src_2 = 180 + src;
    // }
    // //calc the angle distance 
    // diff_1 = abs(turn - src_1)   //normal
    // diff_2 = abs(turn - src_2)   //reverse
    // if (diff_1 > 180)
    // {
    // 	diff_1 = 360 - diff_1;
    // }
    // if (diff_2 > 180)
    // {
    // 	diff_2 = 360 - diff_2;
    // }
    // if (diff_2 >= diff_1)
   	// {
   	// 	return 0;  //normal turn
   	// }
   	// else
   	// {
   	// 	return 1; //reverse turn 
   	// }
   	//思路：由于每次循环都会重新读一次turn，因此修改turn是没有问题的

} 

