/*-----------------------------------------
 File Name : car_test.cpp
 Purpose :
 Creation Date : 04-04-2016
 Last Modified : Mon Apr  4 16:35:21 2016
 Created By : Jeasine Ma
-----------------------------------------*/
#include <iostream>
#include "./catchtest/car_handle.h"

using namespace std;

int main()
{
	CarHandle *car = new CarHandle();
	while(1) {
		car->targetSpeed = 100;
		car->targetAngle = 30;
	}	
}

