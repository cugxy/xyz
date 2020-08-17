//
// Created by cugxy on 2020/7/27.
//

#include <iostream>
#include <cstdlib>
#include <cfloat>

double hmean(double a, double b)
{
    if (a == -b)
    {
        std::cout << "untenable arguments to hmean()\n";
        std::abort();
    }
    return 2.0 * a * b / (a + b);
}

bool hmean(double a, double b, double * ans)
{
    if (a == -b)
    {
        *ans = DBL_MAX;
        return false;
    }
    *ans = 2.0 * a * b / (a + b);
    return true;
}


double hmean1(double a, double b)
{
    if (a == -b)
        throw "Bad hmean() arguments: a = -b not allowed";
    return 2.0 * a * b / (a + b);
}


class BadHmean
{
private:
    double a, b;
public:
    BadHmean(double a, double b): a(a), b(b) {};
    inline void mesg()
    {
        std::cout << "Hmean(" << a << ", " << b << "); invalid arguments a = -b \n";
    }
};

double hmean2(double a, double b)
{
    if (a == -b)
        throw BadHmean(a, b);
    return 2.0 * a * b / (a + b);
}




int main()
{
    double x, y, z;
    std::cout << "Enter two numbers: ";
    while (std::cin >> x >> y)
    {
        z = hmean(x, y);
        std::cout << "Harmonic mean of " << x << " and " << y << " is " << z << std::endl;
    }
    std::cout << "Bye!\n";
    return 0;
}