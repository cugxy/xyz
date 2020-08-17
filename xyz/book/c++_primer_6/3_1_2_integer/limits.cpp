//
// Created by cugxy on 2020/7/19.
//

#include <iostream>
#include <climits>

using std::cout;
using std::endl;
using std::wcout;

void init()
{
    // 初始化
    short year = 1995;
    short year1(1995);
    short year2{1995};      // { } 初始化将越来越常用
    short year3{};          // {} 初始化为 0
    short year4 = {4};
    cout << year << year1 << year2 << year3 << year4 << endl;
}

void limit()
{
    int n_int = INT_MAX;
    short n_short = SHRT_MAX;
    long n_long = LONG_MAX;
    long long n_llong = LONG_LONG_MAX;

    cout << "int is " << sizeof(int) << " bytes." << endl;
    cout << "short is " << sizeof(short) << " bytes." << endl;
    cout << "long is " << sizeof(long) << " bytes." << endl;
    cout << "long long is " << sizeof(long long) << " bytes." << endl;
    cout << endl;

    cout << "Maximum values: " << endl;
    cout << "int:" << n_int << endl;
    cout << "short:" << n_short << endl;
    cout << "long:" << n_long << endl;
    cout << "long long:" << n_llong << endl;
    cout << endl;

    cout << "Minimum int values = " << INT_MIN << endl;
    cout << "Bits per byte = " << CHAR_BIT << endl;
}

#define ZERO 0

void exceed()
{
    short sam = SHRT_MAX;
    unsigned short sue = sam;
    cout << endl;

    cout << "Sam is " << sam << " and sue is " << sue << endl;
    sam++;
    sue++;
    cout << "Sam is " << sam << " and sue is " << sue << endl;

    sam = ZERO;
    sue = ZERO;
    cout << "Sam is " << sam << " and sue is " << sue << endl;
    sam--;
    sue--;
    cout << "Sam is " << sam << " and sue is " << sue << endl;
}

void hexoct()
{
    using std::hex;
    using std::oct;
    int n1 = 42;
    int n2 = 0x42;
    int n3 = 042;
    cout << endl;
    cout << "n1:" << n1 << "(decimal)" << endl;
    cout << hex;
    cout << "n2:" << n2 << "(hexadecimal)" << endl;
    cout << oct;
    cout << "n1:" << n3 << "(octal)" << endl;
}

void unicode()
{
    cout << endl;
    cout << "Let them eat g\u00E2teau.\n";
}

void wchart()
{
    // 用 L 前缀来标识 wchar_t
    // wcin 和 wcout 则可处理 wchar_t 类型的输入输出流.
    wchar_t b = L'P';
    wcout << L"tall" << endl;
    // 用 u 前缀标识 char16_t (无符号 16 位) 用 U 前缀标识 char32_t (无符号 32 位)
    char16_t ch1 = u'q';
    char32_t ch2 = U'\U0000222B';
}

void BOOL_()
{
    cout << endl;
    int ans = true;
    int pro = false;
    cout << ans << ' ' << pro << endl;
}



int main()
{
    init();
    limit();
    exceed();
    hexoct();
    unicode();
    wchart();
    BOOL_();
    return 0;
}
