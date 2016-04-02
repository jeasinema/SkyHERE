#include "car_handle.h"
#include <cstdlib>
#include <cstdio>

using namespace std;

CarHandle::CarHandle(const char *serialName, speed_t baudrate)
{
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

	prev_speed = prev_angle = 0;
}

int CarHandle::sendCmd(int speed, int angle)
{
	if (speed == 0) {
		angle = prev_angle;
		speed = max(0, prev_speed - 5);
	}
	prev_speed = speed;
	prev_angle = angle;

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
