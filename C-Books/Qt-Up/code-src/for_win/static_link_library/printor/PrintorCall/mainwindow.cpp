#if defined __cplusplus
#include <iostream>
#endif

#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "printorref.h" // 引用第三方库

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_testBtn_clicked()
{
    TechiDaily::PrintorRef ref;
#if defined __cplusplus
    std::cout << ref.hi() << std::endl;
#endif

}
