#include "pid.h"
#define MAX_INTEGRATION_ERROR                2500
#define MAX_PID_OUTPUT                       4000


/*调整：
1.电机档位调回4000挡
2.（未做）参照编码器输出调节而不是角度
3.180度处的超调问题




*/
PID Motor_Run={0,0,0,0,0,0,0,0}, Motor_Turn={1,0,100,0,0,0,0,0};  //传参时注意应当取地址
void calcPID(PID *pid, int input)
{
	int output,error;
	error=pid->targetValue-input;	
	if (pid->Ki != 0)
	{
	    pid->integrationError += error;
	    // Limit the maximum integration error
	    if (pid->integrationError > MAX_INTEGRATION_ERROR)
	    {
	        pid->integrationError = MAX_INTEGRATION_ERROR;
	    }
	    else if (pid->integrationError < -MAX_INTEGRATION_ERROR)
	    {
	        pid->integrationError = -MAX_INTEGRATION_ERROR;
	    }
	 }

	output = pid->Kp * error + pid->Ki * pid->integrationError + pid->Kd * (error - pid->lastError);

	// Limit the maximum output
	if (output > MAX_PID_OUTPUT)
	{
	    output = MAX_PID_OUTPUT;
	}
	else if (output < -MAX_PID_OUTPUT)
	{
	    output = -MAX_PID_OUTPUT;
	}

	pid->lastError = error;
	pid->PWM = output;

}
