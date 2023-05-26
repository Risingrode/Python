#include "mainwindow.h"
#include <QApplication>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    MainWindow w;
    w.setFixedSize(800, 600);
    w.setWindowTitle("Amazon");

    w.show();

    return a.exec();
}
