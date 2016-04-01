/*
using trad method to chase the object
*/
#include <opencv2/opencv.hpp>
#include <cstdlib>
#include <unistd.h>
#include <iostream>
#include "lib.h"
#include "car_handle.h"
#include "video_handle.h"

using namespace cv;
using namespace std;

int max_speed = 100;
Result result;
Size re_size(160 ,120);  // first is width
int center_delta = 0;

CarHandle car(0);

int main(int argc, char* argv[])
{
	VideoHandle cam(0);
    cam.selectImageColor();
    destroyAllWindows();
    //sleep(5);
	for (int i = 30; i>0; i--) {
		cam.getImage();
	}
    cout << "start now" << endl;

    while(true) {
        cam.getImage();
        cam.prehandleImage(re_size);

        //cam.prehandle_image()
        cam.findcenterImage();

        //detect the glob
        if (cam.moments.m00 != 0) {
            //cv2.line(cam.frame, (cam.centerx,cam.centery), (x_pre, y_pre), (255,0,0),3)
			//m00 = 10000 -> 70  m00 = 100000 -> 100
			center_delta = ((cam.moments.m00)/1000 - 10)/4 + 14; 
			if (center_delta > 40) {
				center_delta = 40;
			}
            result = cam.generateOutput(Point(re_size.width/2,re_size.height/2+center_delta), Point(cam.centerx,cam.centery));
        } else {
            result = Result(result.angle, 0);
        }
        imshow("catch", cam.mask);
		//imshow("origin", cam.frame);
        waitKey(1);
        /*
        测一下length的大小:(320,0) -> length = 200
        				   (40,0) -> length = 30  speed*=3
    					   (60,0) -> length = 45  speed*=2
        距离小于多少时自动stop？
        ->(120,90) 大约20左右合适
        */
        int speed = result.length*3 + 30;
        if (speed < 60) {
            speed = 0;
        } else {
            speed = (speed - 60) * 2;
        }
        if (speed > max_speed) {
            speed = max_speed;
        }
        cout << result.angle << " " << speed << " (" << cam.centerx << "," << cam.centery << ")" << "," << cam.moments.m00 << "," << center_delta + re_size.height/2 << endl;
		//car.sendCmd(speed, -result.angle); //angle is reerse from the vision of the car
    }
    return 0;
}
