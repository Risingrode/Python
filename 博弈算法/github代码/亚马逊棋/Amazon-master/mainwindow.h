#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QDialog>
#include "amazon.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    amazon *Amazon;

    int stepCount, operateCount, isAI, isBeing, isRunning, Time;
    void paintEvent(QPaintEvent *event);
    void mousePressEvent(QMouseEvent *event);
    void GameRunning();
    void NewGame(); //运行部分
    void AIplay();
    void Record();
    void LoadDoit();
    void Load();
    void Quit();
};

#endif // MAINWINDOW_H
