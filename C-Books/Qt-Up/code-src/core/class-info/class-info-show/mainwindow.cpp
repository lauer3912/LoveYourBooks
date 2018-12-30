#include <iostream>

#include <QMetaClassInfo>
#include <QMetaProperty>
#include <QDebug>

#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // 槽的处理，根据连接的次序，依次执行
    connect(this, SIGNAL(updateMsg(QString &)), this, SLOT(onGetUpdateMsg(QString &)));
    connect(this, SIGNAL(updateMsg(QString &)), this, SLOT(onGetUpdateMsg2(QString &)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_showBtn_clicked()
{
    const int getClassInfoWay = 0;

    if (0 == getClassInfoWay) {
        const QMetaObject* metaObject = this->metaObject();

        std::cout << "metaObject->className() = " << metaObject->className() << std::endl;

        std::cout << "metaObj->classInfo : = " << std::endl;
        for(int i = metaObject->classInfoOffset(); i < metaObject->classInfoCount(); ++i) {
            std::cout << metaObject->classInfo(i).name() << std::endl;
        }
        std::cout << "----------------------"  << std::endl;

        std::cout << "metaObj->property : = " << std::endl;
        for(int i = metaObject->propertyOffset(); i < metaObject->propertyCount(); ++i) {
            std::cout << metaObject->property(i).name() << std::endl;
        }
        std::cout << "----------------------"  << std::endl;

        //QMetaClassInfo const &mcinfo = metaObj->classInfo(0);
    }
}

void MainWindow::on_loopMsgBtn_clicked()
{
    qDebug() << "on_loopMsgBtn_clicked";

    QString message = "Hello";
    emit updateMsg(message);
}

void MainWindow::onGetUpdateMsg(QString& msg) {
    QObject* sender = this->sender();
    qDebug() << "[0]on_get_updateMsg: " << msg;
}
void MainWindow::onGetUpdateMsg2(QString& msg) {
    qDebug() << "[1]on_get_updateMsg: " << msg;
}
