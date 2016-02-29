#include <iostream>
#include "opencv2/core.hpp"
#include "opencv2/opencv.hpp"
#include "opencv2/highgui.hpp"

using namespace cv;
using namespace std;

tuple<Mat, Mat, double> calibrate_fisheye(const vector<Mat>& images, const Settings& s) {
	/*寻找二维角点*/
	auto corners = chessboard_corners(images, s);
	/*计算二维角点对应的三维点坐标*/
	auto object_points = vector<vector<Point3d>>(corners.size(), object_positions(s));
	cv::Matx33d K;
	cv::Vec4d D;
	int flag = 0;
	flag |= cv::fisheye::CALIB_RECOMPUTE_EXTRINSIC;
	flag |= cv::fisheye::CALIB_CHECK_COND;
	flag |= cv::fisheye::CALIB_FIX_SKEW;/*非常重要*/

	double rms = fisheye::calibrate(object_points, 
		corners, 
		s.imageSize,
		K, D, 
		cv::noArray(), cv::noArray(), 
		flag, 
		cv::TermCriteria(3, 20, 1e-6));
	return make_tuple(Mat(K), Mat(D), rms);
}

int main(int, char**)
{
    VideoCapture cap(1); // open the default camera
    if(!cap.isOpened())  // check if we succeeded
        return -1;
    Mat edges;
	namedWindow("edges",1);
    for(;;)
    {
	        Mat frame;
	        cap >> frame; // get a new frame from camera
			//cout << frame << endl;
			cvtColor(frame, edges, COLOR_BGR2GRAY);
	        GaussianBlur(edges, edges, Size(7,7), 1.5, 1.5);
	        Canny(edges, edges, 0, 30, 3);
	        imshow("edges", edges);
	        if(waitKey(30) >= 0) break;
	}

	    // the camera will be deinitialized automatically in VideoCapture destructor
	return 0;
}
