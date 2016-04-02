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
private:
	int serial;
    int prev_speed, prev_angle;
};

#endif // CARHANDLE_H
