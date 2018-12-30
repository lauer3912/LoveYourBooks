#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui
{
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    Q_CLASSINFO("Author", "lauer3912")
    Q_CLASSINFO("Description", "Test Class Information")
    Q_CLASSINFO("Version", "3.0.0")

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

signals:
    void updateMsg(QString &msg);


public slots:
    void onGetUpdateMsg(QString &msg);
    void onGetUpdateMsg2(QString &msg);


private slots:
    void on_showBtn_clicked();
    void on_loopMsgBtn_clicked();

private:
    Ui::MainWindow *ui;
};

class MyClass : public QObject
{

    Q_PROPERTY(Priority priority READ priority WRITE setPriority NOTIFY priorityChanged)

public:
    MyClass(QObject *parent = nullptr);
    ~MyClass();

    enum Priority
    {
        High,
        Low,
        VeryHigh,
        VeryLow
    };
    Q_ENUM(Priority)

    void setPriority(Priority priority) {
        m_priority = priority;
        emit priorityChanged(priority);
    }
    Priority priority() const { return m_priority; }
signals:
    void priorityChanged(Priority);

private:
    Q_OBJECT
    Priority m_priority;
};

#endif // MAINWINDOW_H
