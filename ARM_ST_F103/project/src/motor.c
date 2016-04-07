#include "motor.h"
#include "stm32f10x.h"
#include "stm32f10x_gpio.h"
#include "stm32f10x_tim.h"
#include "delay.h"
#include "encoder.h"
#include "pid.h"

#define PID
#define Max_Val   4000
#define less_val  9    //少转的角度
#define BOTTOMIMPROVE    //串口通信不畅，直接在底层实现转角的优化

//int Target_Speed = 0;
//float Target_Angle = 0;

int abs(int a)
{
	if (a >= 0)
		return a;
	else
		return -a;
}

void Motor_Init(void){
	GPIO_Motor_Config();
	TIM1_Init();
	TIM4_Init();
}

void GPIO_Motor_Config(void){
	  //GPIO³õÊ¼»¯
   	  GPIO_InitTypeDef GPIO_InitStructure;  
	  RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);
	  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA , ENABLE);  
	  RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB , ENABLE);      
	  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_8|GPIO_Pin_9;      
	  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;           
	  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;          
	  GPIO_Init(GPIOA, &GPIO_InitStructure);
	  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6|GPIO_Pin_7;
	  GPIO_Init(GPIOB, &GPIO_InitStructure);
	  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_13|GPIO_Pin_12;
	  GPIO_Init(GPIOB, &GPIO_InitStructure);
}

void TIM4_Init(void){
		//TIM4³õÊ¼»¯
		TIM_TimeBaseInitTypeDef  TIM4_TimeBaseStructure; 
		TIM_OCInitTypeDef  TIM4_OCInitStructure;
		RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM4, ENABLE);   	   
		TIM_DeInit(TIM4);
		TIM4_TimeBaseStructure.TIM_Prescaler = 0xFF;//8????
		TIM4_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;//??????
		TIM4_TimeBaseStructure.TIM_Period = 100;//???????4000
		TIM4_TimeBaseStructure.TIM_ClockDivision = 0x0;//??????1
		TIM4_TimeBaseStructure.TIM_RepetitionCounter = 0; 

			TIM_TimeBaseInit(TIM4,&TIM4_TimeBaseStructure);

		TIM_OCStructInit(&TIM4_OCInitStructure);         
		TIM4_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM2; //?????4???1?PWM1??

		/*Motor 1*/
		TIM4_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;     
		TIM4_OCInitStructure.TIM_OutputNState = TIM_OutputNState_Enable;	
		TIM4_OCInitStructure.TIM_Pulse = 0;  
		TIM4_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_Low;	//???????
		TIM_OC1Init(TIM4,&TIM4_OCInitStructure);	 
		TIM_OC1PreloadConfig(TIM4, TIM_OCPreload_Enable);

		/*Motor 1R*/
		TIM4_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;
		TIM4_OCInitStructure.TIM_Pulse = 0; 
		TIM4_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_Low;
		TIM_OC2Init(TIM4, &TIM4_OCInitStructure);
		TIM_OC2PreloadConfig(TIM4, TIM_OCPreload_Enable); 

		TIM_ARRPreloadConfig(TIM4, ENABLE);

		TIM4->BDTR |= 1<<15;  

		TIM_Cmd(TIM4,ENABLE);
		TIM_CtrlPWMOutputs(TIM4, ENABLE); 
}

void TIM1_Init(){
		TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure; 
		TIM_OCInitTypeDef  TIM_OCInitStructure;
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM1, ENABLE);   	   
		TIM_DeInit(TIM1);
		TIM_TimeBaseStructure.TIM_Prescaler = 0xFF;//8????
		TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;//??????
		TIM_TimeBaseStructure.TIM_Period = 4000;//???????4000
		TIM_TimeBaseStructure.TIM_ClockDivision = 0x0;//??????1

		TIM_TimeBaseInit(TIM1,&TIM_TimeBaseStructure);

		TIM_OCStructInit(&TIM_OCInitStructure);         
		TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM2; //?????4???1?PWM1??
		
		/*Motor 3*/
		TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;           
		TIM_OCInitStructure.TIM_Pulse = 0;  
		TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_Low;	//???????
		TIM_OC1Init(TIM1,&TIM_OCInitStructure);	 
		TIM_OC1PreloadConfig(TIM1, TIM_OCPreload_Enable);

		/*Motor 3R*/
		TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable;
		TIM_OCInitStructure.TIM_Pulse = 0; 
		TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_Low;	
		TIM_OC2Init(TIM1, &TIM_OCInitStructure);
		TIM_OC2PreloadConfig(TIM1, TIM_OCPreload_Enable); 
		
		TIM_ARRPreloadConfig(TIM1, ENABLE);
		
		TIM1->BDTR |= 1<<15;  
		
		TIM_Cmd(TIM1,ENABLE);
		TIM_CtrlPWMOutputs(TIM1, ENABLE);
} 

void Car_Run(int speed)   //speed inrange(-100,100)
{
	speed = - speed;
	if(speed > Max_Val)
		speed = Max_Val;
	if(speed < -Max_Val)
		speed = -Max_Val;
	//#ifndef PID
	if (speed > 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_13);
		TIM_SetCompare1(TIM4, speed);
		TIM_SetCompare2(TIM4, 0);
	}
	else if(speed < 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_13);
		TIM_SetCompare1(TIM4, 0);
		TIM_SetCompare2(TIM4, -speed);
	}
	else 
	{
		TIM_SetCompare1(TIM4, 50);
		TIM_SetCompare2(TIM4, 50);
		Delay(0xFFF);
		GPIO_ResetBits(GPIOB, GPIO_Pin_13);
	}
	//#endif

	// #ifdef PID
	// Motor_Run.targetValue = speed;
	// #endif
}


void Car_Turn(float angle)     //顺逆旋转
{
	if (angle == 0)
	{
		TIM_SetCompare1(TIM1, 4000);
		TIM_SetCompare2(TIM1, 4000);
		Delay(0xFFF);   //刹车时间
		//GPIO_ResetBits(GPIOB, GPIO_Pin_12);

	}
	else if (angle > 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_12);
		TIM_SetCompare1(TIM1, 4000);
		TIM_SetCompare2(TIM1, 0);
	}
	else if (angle < 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_12);
		TIM_SetCompare1(TIM1, 0);
		TIM_SetCompare2(TIM1, 4000);
	}
}

void Car_Turn_Angle(float angle)
{
	int tmp;

	#ifndef PID
	//确定目标值，初步计划少转一点
	if (((angle - Car_Angle) > 180) || ((angle - Car_Angle) < -180))   //正常旋转方向不是最优
	{
		if ((angle - Car_Angle) > 0)   
		{
			angle = angle + less_val;
		}
		else							
		{
			angle = angle - less_val;
		}
	}
	else
	{
		if ((angle - Car_Angle) > 0)   
		{
			angle = angle - less_val;
		}
		else							
		{
			angle = angle + less_val;
		}
		
	}
	if(angle >= 0)
	{
		TIM2->CCR3 = angle / 360 * 4000;
	}
	else
	{
		TIM2->CCR3 = 4000 + angle / 360 * 4000;
	}
	if (((angle - Car_Angle) > 180) || ((angle - Car_Angle) < -180))   //正常旋转方向不是最优
	{
		if ((angle - Car_Angle) > 0)   //本应顺时针，优化为逆时针
		{
			tmp = -1;
		}
		else							//本应逆时针，优化为顺时针
		{
			tmp = 1;
		}
	}
	else
	{
		tmp = angle - Car_Angle;    //正常旋转方向
	}
	Car_Turn(tmp);//正向正转，反向反转
	TIM_ITConfig(TIM2, TIM_IT_CC3, ENABLE);
	#endif
	
	#ifdef PID
	//串口调节不畅，底层直接实现转角优化
	Motor_Turn.targetValue = angle;
	#endif
}


//为保证向下兼容，PID调用此函数
void Car_Turn_Speed(int speed)
{
	//再次限幅
	if (speed > Max_Val)
	{
		speed = Max_Val;
	}
	else if(speed < -Max_Val)
	{
		speed = -Max_Val;
	}

	if(speed > 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_12);
		TIM_SetCompare1(TIM1, speed+200);   //死区约为200
		TIM_SetCompare2(TIM1, 0);
	}
	else if (speed < 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_12);
		TIM_SetCompare1(TIM1, 0);
		TIM_SetCompare2(TIM1, -speed-200);
	}
	else 
	{
		TIM_SetCompare1(TIM1, 4000);
		TIM_SetCompare2(TIM1, 4000);
		Delay(0xFF);   //刹车时间
		GPIO_ResetBits(GPIOB, GPIO_Pin_12);
	}
}

void Car_Run_Speed(int speed)
{
	if (speed > 100)
	{
		speed = 100;
	}
	else if(speed < -100)
	{
		speed = -100;
	}

	if(speed > 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_13);
		TIM_SetCompare1(TIM4, speed);
		TIM_SetCompare2(TIM4, 0);
	}
	else if (speed < 0)
	{
		GPIO_SetBits(GPIOB, GPIO_Pin_13);
		TIM_SetCompare1(TIM4, 0);
		TIM_SetCompare2(TIM4, -speed);
	}
	else 
	{
		TIM_SetCompare1(TIM4, 100);
		TIM_SetCompare2(TIM4, 100);
		Delay(0xFF);   //刹车时间
		GPIO_ResetBits(GPIOB, GPIO_Pin_14);
	}
}

void TIM2_IRQHandler()
{
	 
	//修改CCR3

	// Car_Turn(0);
	// TIM_ITConfig(TIM2, TIM_IT_CC3, DISABLE);
	TIM_ClearITPendingBit(TIM2, TIM_IT_CC3);

	 // USART1_printf(USART2,"aaa\r\n");
	 // USART1_printf(USART2,TIM2->CNT);
	 // USART1_printf(USART2,"\r\n");
	 // USART1_printf(USART2,TIM2->CCR3);
	 // USART1_printf(USART2,"\r\n");
}
