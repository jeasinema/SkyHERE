#ifndef __DELAY_H
#define __DELAY_H

#include "stm32f10x.h"

/*.h.c亦属于不同的文件*/
/*这样的好处是，在其他文件引用该文件中的变量时直接#include即可，不必单独extern*/
extern uint16_t fac_ms;//全局变量
extern uint8_t fac_us;//全局变量

void Delay_Ms(uint16_t nms);
void Delay_Us(uint32_t nus);
void Delay_Init(uint8_t SYSCLK);
void Delay(uint8_t s);

#endif

