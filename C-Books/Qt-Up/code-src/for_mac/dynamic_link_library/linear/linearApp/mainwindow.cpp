#if defined __cplusplus
    #include <iostream>
#endif

#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    //系统默认建立连接
    //connect(this->ui->testButton, SIGNAL(clicked()), this, SLOT(on_testButton_clicked()));

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_testButton_clicked()
{
    std::cout << "Call on_testButton_clicked" << std::endl;
}
