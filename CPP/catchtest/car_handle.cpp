#include "car_handle.h"

CarHandle::CarHandle(char *serialName, speed_t baudrate)
{
	int USB = open(serialName, O_RDWR| O_NOCTTY );
	struct termios tty;
	struct termios tty_old;
	memset (&tty, 0, sizeof tty);

	/* Error Handling */
	if ( tcgetattr ( USB, &tty ) != 0 ) {
	   printf("Error int open the serial"); 
	}

	/* Save old tty parameters */
	tty_old = tty;

	/* Set Baud Rate */
	cfsetospeed (&tty, (speed_t)baudrate);
	cfsetispeed (&tty, (speed_t)baudrate);
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
		printf("Failed to flush the serial port.");
		exit(0);
	}
	serial = USB;
}

int CarHandle::sendCmd(int speed, int angle)
{
	char *cmd;
	sprintf(cmd, "#%d-%d*", speed, angle);
    int n_written = 0 , spot = 0;
	do {
		n_written = write(serial, &cmd[spot], 1 );
		spot += n_written;  //smart!
	} while (cmd[spot-1] != '\r' && n_written > 0);
	return 1;
}
