#include "encoder.h"
#include "motor.h"
#include "stm32f10x.h"
#include "stm32f10x_tim.h"
#include "stm32f10x_gpio.h"
#include "stm32f10x_it.h"
#include "stm32f10x_exti.h"
#include "misc.h"
#include "delay.h"



//Omron Encoder counts for 4000 per spin
#define Startup
//#define angle_CNT   10000  //转一周的计数数

int Car_Speed = 0;
float Car_Angle = 0; 
uint8_t Start_Due = 0;
int32_t zero = 0;   //启动时标定，起始位置的相对编码器值
uint8_t Angle_Target_Interrupt = 100;   //中断实现特定角度旋转

void TIM3_Init()    //运动电机
{

	//u16 CCR1_Val = 2500;
	//u16 CCR2_Val = 1000;
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	TIM_ICInitTypeDef TIM_ICInitStructure;
	//TIM_OCInitTypeDef  TIM_OCInitStructure;

	/*----------------------------------------------------------------*/

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);


	GPIO_StructInit(&GPIO_InitStructure);
	/* Configure PA.06,07 as encoder input */
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	/*----------------------------------------------------------------*/	


	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE); //使能ＴＩＭ３
	TIM_DeInit(TIM3);
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);

	TIM_TimeBaseStructure.TIM_Period =8000;       //此处设置所使用的编码器转一圈产生的计数
	TIM_TimeBaseStructure.TIM_Prescaler =0;	    //设置预分频：
	TIM_TimeBaseStructure.TIM_ClockDivision =TIM_CKD_DIV1 ;	//设置时钟分频系数：不分频
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;  //向上计数模式
	//TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_CenterAligned1; 
	/*初始化TIM3定时器 */
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);

	/*-----------------------------------------------------------------*/
	//编码配置                        编码模式
	TIM_EncoderInterfaceConfig(TIM3, TIM_EncoderMode_TI12, 
	                         TIM_ICPolarity_Rising, TIM_ICPolarity_Rising);  //TIM_ICPolarity_Rising上升沿捕获
	TIM_ICStructInit(&TIM_ICInitStructure);
	TIM_ICInitStructure.TIM_ICFilter = 1;         //比较滤波器
	TIM_ICInit(TIM3, &TIM_ICInitStructure);

	TIM_ClearFlag(TIM3, TIM_FLAG_Update);
	TIM_ITConfig(TIM3, TIM_IT_Update, ENABLE);   //使能中断
	//Reset counter
	TIM3->CNT =0;


	TIM_Cmd(TIM3, ENABLE);   //使能定时器3



}

void TIM2_Init()   //转向电机
{
	

	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef  TIM_TimeBaseStructure;
	TIM_ICInitTypeDef TIM_ICInitStructure;
	TIM_OCInitTypeDef  TIM_OCInitStructure;
	NVIC_InitTypeDef   NVIC_InitStructure; 

	/*----------------------------------------------------------------*/

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);


	GPIO_StructInit(&GPIO_InitStructure);
	/* Configure PA.06,07 as encoder input */
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	/*----------------------------------------------------------------*/	


	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE); //使能ＴＩＭ３
	TIM_DeInit(TIM2);
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseStructure);

	TIM_TimeBaseStructure.TIM_Period =4000;       
	TIM_TimeBaseStructure.TIM_Prescaler =0;	    //设置预分频：
	TIM_TimeBaseStructure.TIM_ClockDivision =TIM_CKD_DIV1 ;	//设置时钟分频系数：不分频
	TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;  //向上计数模式
	//TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_CenterAligned1; 
	/*初始化TIM3定时器 */
	TIM_TimeBaseInit(TIM2, &TIM_TimeBaseStructure);

	/*-----------------------------------------------------------------*/
	//编码配置                        编码模式
	TIM_EncoderInterfaceConfig(TIM2, TIM_EncoderMode_TI12, 
	                         TIM_ICPolarity_Rising, TIM_ICPolarity_Rising);  //TIM_ICPolarity_Rising上升沿捕获
	TIM_ICStructInit(&TIM_ICInitStructure);
	TIM_ICInitStructure.TIM_ICFilter = 1;         //比较滤波器
	TIM_ICInit(TIM2, &TIM_ICInitStructure);
   
	TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_Timing; 
	TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Disable; 
	TIM_OCInitStructure.TIM_Pulse = Angle_Target_Interrupt;
	TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;
	TIM_OC3Init(TIM2, &TIM_OCInitStructure);
	TIM_OC3PreloadConfig(TIM2, TIM_OCPreload_Disable);//禁止 TIM_CCR1 寄存器的预装载使能
	TIM_ITConfig(TIM2, TIM_IT_CC3, DISABLE);//中断使能 TIM_Cmd(TIM2, ENABLE); //开启定时器(即设置 CEN 位)




	// TIM_OCStructInit(&TIM_OCInitStructure);       //中断实现特定角度转动的配置
	// TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_Timing;
	// TIM_OCInitStructure.TIM_Pulse = Angle_Target_Interrupt;
	// TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;
	// TIM_OC3Init(TIM2, &TIM_OCInitStructure);
	// TIM_OC3PreloadConfig(TIM2, TIM_OCPreload_Disable);
	// TIM_ITConfig(TIM2, TIM_IT_CC3, ENABLE);

	TIM_ClearFlag(TIM2, TIM_FLAG_CC3);
	TIM_ITConfig(TIM2, TIM_IT_Update, DISABLE);   //使能中断
	//Reset counter
	TIM2->CNT = 0;   


	TIM_Cmd(TIM2, ENABLE);   //使能定时器3

	/* Enable the TIM2 Interrupt */
    NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;
    NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0;
    NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC_Init(&NVIC_InitStructure);   
}

void EXTI4_Encoder_Init()
{
	GPIO_InitTypeDef  GPIO_InitStructure;  
    EXTI_InitTypeDef exti;  
    NVIC_InitTypeDef NVIC_exti;  
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);            //挂载IO口德时钟   
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE); //挂载复用IO的辅助功能时钟                                                   
    //GPIO配置上拉输入  A
    GPIO_InitStructure.GPIO_Pin =GPIO_Pin_4;  
    GPIO_InitStructure.GPIO_Mode =  GPIO_Mode_IPU;      //上拉与上升沿对应  
    GPIO_Init(GPIOA,&GPIO_InitStructure);  
              
    //GPIO引脚与中断线的映射关系  
    GPIO_EXTILineConfig(GPIO_PortSourceGPIOA,GPIO_PinSource4);  
      
    //exti配置  
    exti.EXTI_Line = EXTI_Line4;  
    exti.EXTI_Mode = EXTI_Mode_Interrupt;            //模式有中断模式和事件模式  
    exti.EXTI_Trigger = EXTI_Trigger_Rising_Falling;  
    exti.EXTI_LineCmd = ENABLE;  
    EXTI_Init(&exti);  
      
    //NVIC中断控制配置  
    NVIC_exti.NVIC_IRQChannel = EXTI4_IRQn;  
    NVIC_exti.NVIC_IRQChannelPreemptionPriority = 0x01;         //抢占优先级是2  
    NVIC_exti.NVIC_IRQChannelSubPriority = 0x01;            //子优先级是2  
    NVIC_exti.NVIC_IRQChannelCmd = ENABLE;  
    NVIC_Init(&NVIC_exti);        
}

void EXTI4_IRQHandler(void)
{
	//USART1_printf(USART2, "%d\r\n",TIM2->CNT);
	//启动自动完成编码器角度标定  (由于转向电机不能很好的伺服，故该操作效果不明显)
	#ifdef Startup
	if (!Start_Due)
	{
		zero = TIM2->CNT; 
		Car_Turn(0); 
		SysTick_Init(72); 
		Start_Due = 1;
		Delay(0xF);
		Car_Turn_Angle(0);   //回零点
	}
	else
	{
		TIM2 -> CNT = zero;   //自动标0，防止编码器发生偏移
	}
	#endif 

	#ifndef Startup
	//TIM2 -> CNT = zero;    //手动标定
	#endif

	EXTI_ClearITPendingBit(EXTI_Line4);
}



void Encoder_Init(void){
	TIM3_Init();
	TIM2_Init();
	EXTI4_Encoder_Init();
}
