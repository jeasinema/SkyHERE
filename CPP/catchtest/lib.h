#ifndef LIB_H
#define LIB_H

#define PI (3.141592653589793)

struct Result
{
    int angle;
    int length;
    Result(){}
    Result(int angle, int length): angle(angle), length(length) {}
};

#endif // LIB_H
