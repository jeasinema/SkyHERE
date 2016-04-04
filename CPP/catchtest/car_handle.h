#ifndef CARHANDLE_H
#define CARHANDLE_H

#include <stdio.h>      // standard input / output functions
#include <stdlib.h>
#include <string.h>     // string function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions
#include <string>
#include "opencv2/opencv.hpp"

using namespace cv;

class CarHandle
{
public:
    CarHandle(const char* serialName = "/dev/ttyUSB0", speed_t baudrate = B9600);
	~CarHandle() {
		sendCmd(0 ,0);
		if (serial) {
			close(serial);
		}
	}
	int sendCmd(int speed, int angle);
	void generateSpeed();
	void scheduler();
	int targetSpeed = 0, targetAngle = 0, PWM = 0;
private:
	int serial;
	int now_speed = 0;
	float Kp = 0;
	int now_time = 0, pre_time = 0;
};

#endif // CARHANDLE_H
