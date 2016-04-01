#include "video_handle.h"
#include <cmath>
#include <csignal>

VideoHandle* VideoHandle::instance = new VideoHandle();

void VideoRelease(int)
{
    VideoHandle* ins = VideoHandle::getInstance();
	if (ins->cap->isOpened()) {
		ins->cap->release();
		cout << "camera has been released." << endl;
	}
    exit(0);
}

void onMouse(int event, int x, int y, int, void* h)
{
    VideoHandle* handle = (VideoHandle*)(h);
    handle->select_color = handle->frame.at<Vec3b>(y,x);
    Mat hsv_image = handle->frame.clone();
    cvtColor(handle->frame, hsv_image, COLOR_BGR2HSV);
    handle->select_color_hsv = hsv_image.at<Vec3b>(y,x);
    if(event == EVENT_LBUTTONDOWN) {
        circle(handle->frame, Point(x, y), 10, Scalar(255, 0, 0), 1);
        handle->selectx = x;
        handle->selecty = y;
        handle->flag_select = true;
        waitKey(50);
    }

    cout << x << " " << y << " " << handle->select_color << " " << handle->select_color_hsv << endl;
}

extern Mat distortmtx = (Mat_<double>(3,3)<<
    411.8740606 ,    0.0        ,  303.41061317,
    0.0         ,  409.43354707 ,  253.78413993,
    0.0         ,    0.0        ,    1.0        );
extern Mat distortdist = (Mat_<double>(1,5) << -0.70529664,  0.62594239, -0.00286203, -0.00662238, -0.29993423);

VideoHandle::VideoHandle(int device)
{
	cap = new VideoCapture(device);
    if (cap->isOpened()) {
        camerawidth = (int)cap->get(CV_CAP_PROP_FRAME_WIDTH);
        cameraheight = (int)cap->get(CV_CAP_PROP_FRAME_HEIGHT);
    } else {
        cerr << "Camera is not correctly init." << endl;
    }
    flag_select = false;
	signal(SIGINT, &VideoRelease);
}

Result VideoHandle::getDirection()
{
    vector<Point> List;
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
        Moments m = ::moments(temp);
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
        if(sum.x*sum.x + sum.y*sum.y >= 30) {
            Result ret = generateOutput(p, Point(p.x+sum.x, p.y+sum.y));
            ret.angle *= -1;
            return ret;
        }
        line(result, p, Point(p.x+sum.x,p.y+sum.y), Scalar(100, 100, 100));

        int now_clock = clock();
        double speed = double(now_clock - prev_clock) / CLOCKS_PER_SEC;
        cout << "speed : " << speed << " " << (1.0/speed) << endl;
    }
}

void VideoHandle::selectImageColor()
{
    flag_select = false;
    namedWindow("select_color");
    setMouseCallback("select_color", onMouse, this);

    while(!flag_select) {
        getImage();
        Mat temp = frame.clone();
        undistort(frame, temp, distortmtx, distortdist);
        frame = temp;
        showImage("select_color");
    }

    cout << selectx << " " << selecty << endl;
    cout << select_color_hsv << endl;
    destroyWindow("select_color");
}

void VideoHandle::prehandleImage(Size size)
{
    //undistort
    {
        Mat temp = frame.clone();
        undistort(temp, frame, distortmtx, distortdist);
    }
    //resize
    resize(frame, frame_resize, size);

    //2HSV
    cvtColor(frame_resize, frame_resize_hsv, COLOR_BGR2HSV);

    //threshold
    // thresholdlow = (Mat_<uchar>(1,3) << select_color_hsv[0]-20, 90, 30);   //no human-light -> 20(unstable); with human-light -> 40
    // thresholdhigh = (Mat_<uchar>(1,3) << select_color_hsv[0]+20, 255, 255);
    thresholdlow = (Mat_<uchar>(1,3) << 115-20, 90, 30);   //no human-light -> 20(unstable); with human-light -> 40
    thresholdhigh = (Mat_<uchar>(1,3) << 115+20, 255, 255);
    inRange(frame_resize_hsv, thresholdlow, thresholdhigh, mask);

    //morphlogy
    {
        Mat temp = mask.clone();
        morphologyEx(temp, mask, MORPH_OPEN, Mat::ones(3, 3, CV_8U));
    }
}

void VideoHandle::findcenterImage()
{
    moments = ::moments(mask);

    if (moments.m00 != 0) {
        centerx = (int)((float)(moments.m10)/(float)(moments.m00));
        centery = (int)((float)(moments.m01)/(float)(moments.m00));
    } else {
        centerx = camerawidth/2;
		centery = cameraheight/2;
    }
}

Result VideoHandle::generateOutput(Point p1, Point p2)
{
    int length = 0;
    double angle = 0;
    //length = np.linalg.norm([p2['x']-p1['x'],p2['y']-p1['y']]) FIXME
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

void VideoHandle::getImage()
{
    (*VideoHandle::cap) >> frame;
}

void VideoHandle::showImage(const string& winname)
{
    imshow(winname, frame);
    waitKey(1);
}

Mat VideoHandle::getUndistortFrame()
{
    Mat temp, frame;
    *cap >> temp;
    if(temp.empty()) return temp;
    undistort(temp, frame, distortmtx, distortdist);
    return frame;
}
