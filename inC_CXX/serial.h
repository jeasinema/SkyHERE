/*-----------------------------------------
 File Name : serial.h
 Purpose :
 Creation Date : 29-03-2016
 Last Modified : Tue Mar 29 00:40:07 2016
 Created By : Jeasine Ma
-----------------------------------------*/
#ifndef _SERIAL_H_
#define _SERIAL_H_

int serialInit(char *serialName, unsigned int baudRate);
unsigned int serialWrite(char *cmd. int USB);
char* serialRead(int USB);

#endif
