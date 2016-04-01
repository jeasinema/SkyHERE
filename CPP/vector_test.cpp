#include <opencv2/opencv.hpp>
#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <ctime>
#include <vector>
#include "catchtest/car_handle.h"
#include <unistd.h>
#include "catchtest/lib.h"

using namespace std;
using namespace cv;

extern Mat distortmtx;
extern Mat distortdist;

VideoCapture cap(0);

vector<Point> List;

CarHandle car;

Mat getUndistortFrame()
{
    Mat temp, frame;
    cap >> temp;
    if(temp.empty()) return temp;
    undistort(temp, frame, distortmtx, distortdist);
    return frame;
}

Result generateOutput(Point p1, Point p2)
{
    int length = 0;
    double angle = 0;
	length = sqrt(pow((p1.x-p2.x), 2) + pow((p1.y-p2.y),2));
    if (p1.x == p2.x) {
        angle = (p2.y > p1.y) ? 180 : 0;
    } else if (p1.y == p2.y) {
        angle = (p2.x > p1.x) ? 90 : -90;
    } else {
        angle = atan(((float)(p2.x-p1.x))/((float)(p1.y-p2.y)));
		angle = (float)(angle) / PI * 180;
        if (p2.y > p1.y) {
            angle = (p2.x > p1.x) ? (180 + angle) : (-180 + angle);
        }
    }
    return Result(angle, length);
}

int main(int argc, char* argv[])
{
    if(!cap.isOpened()) {
        return -1;
    }

    Mat frame;
    Mat prev;

    getUndistortFrame();
    getUndistortFrame();
    prev = getUndistortFrame();

    while(true)
    {
        int prev_clock = clock();

        frame = getUndistortFrame();
        if(frame.empty()) break;

        Mat temp;
        subtract(prev, frame, temp);
        resize(temp, temp, Size(120,90), 0, 0, CV_INTER_LINEAR);
        cvtColor(temp, temp, CV_BGR2GRAY);
        threshold(temp, temp, 20, 255, CV_THRESH_BINARY);

        Mat result = Mat::zeros(temp.size(), CV_8UC3);
        Moments m = moments(temp);
        Point p = Point(m.m10/m.m00, m.m01/m.m00);
        circle(result, p, 1,Scalar(255, 255, 255));

        cout << "Point : " << p.x << " " << p.y << endl;
        List.push_back(p);
        if (p.x < 10 || p.y < 5 || p.x > 110 || p.y > 85) {
            cout << "233333333333333" << endl;
            List.clear();
        }

        const int TIMES = 3;
        Point sum = Point(0, 0);
        for(int i=1;i<=TIMES;i++)
        {
            if(List.size() < TIMES + 1) continue;
            Point a = List[List.size() - i];
            Point b = List[List.size() - i - 1];
            Point sub = Point(a.x-b.x, a.y-b.y);
            sum.x += sub.x;
            sum.y += sub.y;
        }

        sum.x /= TIMES;
        sum.y /= TIMES;

        cout << "vector : " << sum.x << " " << sum.y << endl;
        if(sum.x*sum.x + sum.y*sum.y >= 40) {
            Result ret = generateOutput(p, Point(p.x+sum.x, p.y+sum.y));
            car.sendCmd(80, -ret.angle);
            sleep(1);
            car.sendCmd(0, 0);
            cout << "catch vector" << endl;
            sleep(1);
            exit(0);
        }
        line(result, p, Point(p.x+sum.x,p.y+sum.y), Scalar(100, 100, 100));

        int now_clock = clock();
        double speed = double(now_clock - prev_clock) / CLOCKS_PER_SEC;
        cout << "speed : " << speed << " " << (1.0/speed) << endl;
    }

    return 0;
}
