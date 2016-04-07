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

VideoCapture video_cap("front.avi");

vector<Point> List;

Size re_size(160,120);   // 增大画幅，解决高抛物体的运动方向无法被识别的问题
//CarHandle car;

Mat getUndistortFrame()
{
    Mat temp, frame;
    video_cap >> temp;
    if(temp.empty()) return temp;
    undistort(temp, frame, distortmtx, distortdist);
    return frame;
}

Mat getFrame()
{
    Mat temp, frame;
    video_cap >> temp;
    return temp;
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
    //if(!video_cap.isOpened()) {
    //    return -1;
    //}

    Mat frame;
    Mat prev;

	for (int i=10;i--;)
		getUndistortFrame();
    //prev = getUndistortFrame();
    prev = getFrame();

    int index = 0;
    while(true)
    {
        index ++;
        int prev_clock = clock();

        //frame = getUndistortFrame();
        frame = getFrame();
		Mat undistort_frame = frame.clone();
		undistort(frame, undistort_frame, distortmtx, distortdist);
        if(frame.empty()) break;

        Mat temp, temp_substract;
        subtract(prev, frame, temp);
		temp_substract = temp.clone();
        resize(temp, temp, re_size, 0, 0, CV_INTER_LINEAR);
        cvtColor(temp, temp, CV_BGR2GRAY);
        threshold(temp, temp, 20, 255, CV_THRESH_BINARY);

		Mat temp_temp = temp.clone();
        morphologyEx(temp_temp, temp, MORPH_OPEN, Mat::ones(3, 3, CV_8U));

		Mat result = Mat::zeros(temp.size(), CV_8UC3);
        Moments m = moments(temp);

        Point p = Point(m.m10/m.m00, m.m01/m.m00);

        circle(result, p, 5,Scalar(0, 0, 255));
		//Mat_<Point2f> points(1,1), dst(1,1);
		//points(0) = Point2f(p.x,p.y);
		//undistortPoints(points, dst, distortmtx, distortdist);
		//Point p = Point(*(r.begin<double>()).x,*(r.begin<double>()).y);
		//p.x = - dst(0).y * re_size.width;
		//p.y = - dst(0).x * re_size.height;
        //circle(result, p, 1,Scalar(255, 255, 255));
        cout << "Point : " << p.x << " " << p.y << endl;

        List.push_back(p);
        if (p.x < 5 || p.y < 5 || p.x > re_size.width - 5|| p.y > re_size.height-5) {
            cout << "233333333333333" << endl;
            List.clear();
        }

        const int TIMES = 2;
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

		Result dir;
		{
			dir = generateOutput(p, Point(p.x+sum.x,p.y+sum.y));
			cout << "vector : " << sum.x << " " << sum.y << " "<< "dir: " << dir.angle <<endl;
		}

		if(sum.x*sum.x > 4 || sum.y*sum.y > 4) {
			getchar(); // FIXME
		}
       //     Result ret = generateOutput(p, Point(p.x+sum.x, p.y+sum.y));
       //     car.sendCmd(80, -ret.angle);
       //     sleep(1);
       //     car.sendCmd(0, 0);
       //     cout << "catch vector" << endl;
       //     sleep(1);
       //     exit(0);
       // }
        line(result, p, Point(p.x+sum.x,p.y+sum.y), Scalar(0, 255, 0),2);
		imshow("origin", frame);
		imshow("subtract", temp);
		imshow("result",result);
		imshow("undistort_frame",undistort_frame);
		imshow("subtract_frame", temp_substract);

        {
            char name[1024];
            sprintf(name, "origin%d.png", index);
            imwrite(name, frame);
            sprintf(name, "substract%d.png", index);
            imwrite(name, temp);
            sprintf(name, "result%d.png", index);
            imwrite(name, result);
            sprintf(name, "un_frame%d.png", index);
            imwrite(name, undistort_frame);
        }
		waitKey(10);

        int now_clock = clock();
        double speed = double(now_clock - prev_clock) / CLOCKS_PER_SEC;
        cout << "speed : " << speed << " " << (1.0/speed) << endl;
    }

    return 0;
}
