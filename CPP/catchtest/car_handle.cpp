#include "car_handle.h"
#include <cstdlib>
#include <cstdio>
#include <ctime>
#include <thread>

#define MAX_PID_OUTPUT                       100
#define INTERRUPT_DELAY						 30000

using namespace std;

CarHandle::CarHandle(const char *serialName, speed_t baudrate)
{
	thread pid_interrupts (&CarHandle::scheduler,this);
	pid_interrupts.detach();
	int USB = open(serialName, O_RDWR| O_NOCTTY);
	struct termios tty;
	struct termios tty_old;
	memset (&tty, 0, sizeof tty);

	/* Error Handling */
	if ( tcgetattr ( USB, &tty ) != 0 ) {
	   std::cout << "Error " << errno << " from tcgetattr: " << strerror(errno) << std::endl;
	}

	/* Save old tty parameters */
	tty_old = tty;

	/* Set Baud Rate */
	cfsetospeed (&tty, (speed_t)B9600);
	cfsetispeed (&tty, (speed_t)B9600);

	/* Setting other Port Stuff */
	tty.c_cflag     &=  ~PARENB;            // Make 8n1
	tty.c_cflag     &=  ~CSTOPB;
	tty.c_cflag     &=  ~CSIZE;
	tty.c_cflag     |=  CS8;

	tty.c_cflag     &=  ~CRTSCTS;           // no flow control
	tty.c_cc[VMIN]   =  1;                  // read doesn't block
	tty.c_cc[VTIME]  =  5;                  // 0.5 seconds read timeout
	tty.c_cflag     |=  CREAD | CLOCAL;     // turn on READ & ignore ctrl lines

	/* Make raw */
	cfmakeraw(&tty);

	/* Flush Port, then applies attributes */
	tcflush( USB, TCIFLUSH );
	if ( tcsetattr ( USB, TCSANOW, &tty ) != 0) {
		std::cout << "Error " << errno << " from tcsetattr" << std::endl;
	}
	serial = USB;
}

int CarHandle::sendCmd(int speed, int angle)
{
//	if (speed == 0) {
//		angle = prev_angle;
//		speed = max(0, prev_speed - 5);   //防止接取过程中偶尔出现的0速度导致的刹车问题
//	}
//	prev_speed = speed;
//	prev_angle = angle;

	printf("[cmd] speed: %d angle: %d\n", speed, angle);

	char cmd[1024];
	sprintf(cmd, "#%d-%d*\r", speed, angle);
    int n_written = 0,
		    spot = 0;
	do {
	    n_written = write(serial, &cmd[spot], 1 );
	    spot += n_written;
	} while (cmd[spot-1] != '\r' && n_written > 0);
	return 1;
}

void CarHandle::generateSpeed()
{
	int output,error;
	error = targetSpeed - now_speed;	

	output = Kp * error;

	// Limit the maximum output
	if (output > MAX_PID_OUTPUT) {
	    output = MAX_PID_OUTPUT;
	} else if (output < -MAX_PID_OUTPUT) {
	    output = -MAX_PID_OUTPUT;
	}
	if(!output) {
		output = 1;
	}
	now_speed += output;
	if (now_speed > MAX_PID_OUTPUT) {
		now_speed = MAX_PID_OUTPUT;
	}
	PWM = now_speed;
	sendCmd(PWM, targetAngle);
}

void CarHandle::scheduler()
{
	while(true) {
		now_time = clock();
		if (((now_time - pre_time) % INTERRUPT_DELAY) == 0) {
			thread genOutput (&CarHandle::generateSpeed,this);
			genOutput.join();
			pre_time = now_time;
		}
	}

}
