#ifndef __COMMUNICATION_H
#define	__COMMUNICATION_H

#include <stdio.h>
#include "stm32f10x_usart.h"


#define USART1_DR_Base  0x40013804

#define Buffer_Size 20

extern uint8_t Cmd_Ble[Buffer_Size];
extern uint8_t Buff_Ble[20];


void USART2_Config(void);
void USART3_Config(void);
int fputc(int ch, FILE *f);
void USART1_printf(USART_TypeDef* USARTx, uint8_t *Data,...);
void DMA_Config(void);
static void NVIC_Config(void);

//__asm SystemReset(void);

#endif 
