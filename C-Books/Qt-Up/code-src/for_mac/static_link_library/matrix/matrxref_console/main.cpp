
#if defined __cplusplus
    #include <iostream>
#endif

#include <QCoreApplication>
#include "matrixref.h" // 引用静态库的头文件

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    TechiDaily::Matrixref ref;

#if defined __cplusplus
    std::cout << ref.hi() << std::endl;
#endif

    return a.exec();
}
