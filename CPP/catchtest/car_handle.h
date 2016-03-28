#ifndef CARHANDLE_H
#define CARHANDLE_H

#include "opencv2/opencv.hpp"

using namespace cv;

class CarHandle
{
public:
    CarHandle(int device = 0, int baudrate = 9600);

    void sendCmd(int speed, int angle);
};

#endif // CARHANDLE_H
