#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "ui_dialog.h"
#include <QPixmap>
#include <QPainter>
#include <QMainWindow>
#include <QMouseEvent>
#include <iostream>
#include <iomanip>
#include <QAction>
#include <QPushButton>
#include <QMessageBox>
#include <QDialog>

MainWindow :: MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui :: MainWindow)
{
    ui -> setupUi(this);

//定义各种键
    //主功能键
    connect(ui -> newGameButton, &QPushButton :: clicked, [this] { NewGame(); });
    connect(ui -> quitButton, &QPushButton :: clicked, [this] { Quit(); });
    connect(ui -> recordButton, &QPushButton :: clicked, [this] { Record(); });
    connect(ui -> loadButton, &QPushButton :: clicked, [this] { Load(); });

    //次级键
    connect(ui -> Level0Button, &QPushButton :: clicked, [this] { //"简单"键

        ui -> askingLevelLabel -> setVisible(false);
        ui -> Level0Button -> setVisible(false);
        ui -> Level1Button -> setVisible(false);
        ui -> Level2Button -> setVisible(false);

        Amazon -> level = 0;

        ui -> widget -> raise(); //按键位置重叠, 需要把它的优先级调高
        ui -> askingColorLabel -> setVisible(true); //决定先后手
        ui -> blackButton -> setVisible(true);
        ui -> whiteButton -> setVisible(true);

        return;
    });

    connect(ui -> Level1Button, &QPushButton :: clicked, [this] { //"中等"键

        ui -> askingLevelLabel -> setVisible(false);
        ui -> Level0Button -> setVisible(false);
        ui -> Level1Button -> setVisible(false);
        ui -> Level2Button -> setVisible(false);

        Amazon -> level = 1;

        ui -> widget -> raise();
        ui -> askingColorLabel -> setVisible(true); //决定先后手
        ui -> blackButton -> setVisible(true);
        ui -> whiteButton -> setVisible(true);

        return;
    });

    connect(ui -> Level2Button, &QPushButton :: clicked, [this] { //"困难"键

        ui -> askingLevelLabel -> setVisible(false);
        ui -> Level0Button -> setVisible(false);
        ui -> Level1Button -> setVisible(false);
        ui -> Level2Button -> setVisible(false);

        Amazon -> level = 2;

        ui -> widget -> raise();
        ui -> askingColorLabel -> setVisible(true); //决定先后手
        ui -> blackButton -> setVisible(true);
        ui -> whiteButton -> setVisible(true);

        return;
    });

    connect(ui -> nextButton, &QPushButton :: clicked, [this] { //"对方落子"键 人机对战专用

        if (clock() < Time + 300) {
            Time = clock();
            std :: cerr << Time << std :: endl;
            return;
        };
        Time = clock(); //加时间戳防止在瞬时内多次按键导致连下多步

        if (!isAI) return;

        ui -> nextButton -> setVisible(false);
        ui -> retryButton -> setVisible(false);

        Amazon -> DecisionMaking(); //AI操作
        Amazon -> ReCordRecord(), ++operateCount;

        ui->recordButton->setVisible(true);

        Amazon -> Initialize(); //接下来玩家操作
        Amazon -> ReCordLoad();
        repaint();

        if (!Amazon -> Judge()) {
           if (isRunning) {
               QMessageBox :: information(this, tr("游戏结束"), tr("AI获胜"));

               isRunning = false;
               ui->recordButton->setVisible(false); //游戏结束时不可存档
               ui -> replaceButton -> setVisible(false); //游戏结束时关闭AI辅助键
           }

           return;
        }

        isBeing = true, isAI = false; //往后可以鼠标输入
        ui -> replaceButton -> raise();
        ui -> replaceButton -> setVisible(true);

        return;
    });

    connect(ui -> retryButton, &QPushButton :: clicked, [this] { //"重新落子"键

        if (!isAI) return;
        ui->nextButton->setVisible(false);
        ui->retryButton->setVisible(false);

        Amazon -> ReCordWithDraw(), --operateCount; //悔步(仅供操作失误的情况使用)
        if (!operateCount) ui->recordButton->setVisible(false);

        Amazon -> Initialize(); //接下来玩家重新操作
        Amazon -> ReCordLoad();
        repaint();

        if (!Amazon -> Judge()) {
            if (isRunning) {
                QMessageBox :: information(this, tr("游戏结束"), tr("AI获胜"));

                isRunning = false;
                ui->recordButton->setVisible(false); //游戏结束时不可存档
                ui -> replaceButton -> setVisible(false); //游戏结束时关闭AI辅助键
            }

            return;
        }

        isBeing = true, isAI = false; //往后可以鼠标输入
        ui -> replaceButton -> raise();
        ui -> replaceButton -> setVisible(true);

        return;
    });

    connect(ui -> replaceButton, &QPushButton :: clicked, [this] { //"AI代替落子"键

        if (clock() < Time + 300) {
            Time = clock();
            std :: cerr << Time << std :: endl;
            return;
        };
        Time = clock(); //加时间戳防止在瞬时内多次按键导致连下多步

        if (!isBeing) return;

        Amazon -> Initialize();
        Amazon -> ReCordLoad();
        Amazon -> level = 2; //用最好的AI代替玩家落子, 改善游戏体验

        Amazon -> DecisionMaking(); //AI操作
        Amazon -> ReCordRecord(), ++operateCount;

        ui->recordButton->setVisible(true);

        isBeing = false, isAI = true;
        AIplay(); //接下来AI操作

        return;
    });

    connect(ui -> blackButton, &QPushButton :: clicked, [&] { //"黑"键 (NewGame专用)
        //It means that "HumanColor = 1"

        ui -> askingColorLabel -> setVisible(false);
        ui -> blackButton -> setVisible(false);
        ui -> whiteButton -> setVisible(false);

        isRunning = true;

        Amazon -> ReCordInitialize(); //初始化棋局, 确定游戏难度

        Amazon -> Initialize(); //接下来玩家操作
        Amazon -> ReCordLoad();
        repaint();

        isBeing = true, isAI = false; //开启鼠标输入
        ui -> replaceButton -> raise();
        ui -> replaceButton -> setVisible(true);

        return;
    });

    connect(ui -> whiteButton, &QPushButton :: clicked, [&] { //"白"键 (NewGame专用)
        //It means that "HumanColor = -1"

        ui -> askingColorLabel -> setVisible(false);
        ui -> blackButton -> setVisible(false);
        ui -> whiteButton -> setVisible(false);

        isRunning = true;

        Amazon -> ReCordInitialize(); //初始化棋局, 确定游戏难度

        isAI = true, isBeing = false; //AI操作
        AIplay();

        return;
    });

    connect(ui -> blackButton2, &QPushButton :: clicked, [&] { //"黑"键 (Load专用)
        //It means that "HumanColor = 1"

        isRunning = true;

        ui -> showingLabel -> setVisible(false);
        ui -> askingColorLabel2 -> setVisible(false);
        ui -> blackButton2 -> setVisible(false);
        ui -> whiteButton2 -> setVisible(false);

        if (Amazon -> curBotColor == 1) { //玩家先手, 这里需要判断是否可以继续游戏

            Amazon -> Initialize(); //玩家操作
            Amazon -> ReCordLoad();
            repaint();

            if (!Amazon -> Judge()) { //游戏结束
                if (isRunning) {
                    QMessageBox :: information(this, tr("消息框"), tr("游戏结束, AI获胜"));

                    isRunning = false;
                    ui->recordButton->setVisible(false); //游戏结束时不可存档
                    ui -> replaceButton -> setVisible(false); //游戏结束时关闭AI辅助键
                }

                return;
            }

            isBeing = true, isAI = false; //接下来开启鼠标操作
            ui -> replaceButton -> raise();
            ui -> replaceButton -> setVisible(true);
        }
        else { //AI先手
            isAI = true, isBeing = false;
            AIplay(); //AI操作
        }

        return;
    });

    connect(ui -> whiteButton2, &QPushButton :: clicked, [&] {
        //It means that "HumanColor = -1"

         isRunning = true;

         ui -> showingLabel -> setVisible(false);
         ui -> askingColorLabel2 -> setVisible(false);
         ui -> blackButton2 -> setVisible(false);
         ui -> whiteButton2 -> setVisible(false);

         if (Amazon -> curBotColor == -1) { //玩家先手, 这里需要判断是否可以继续游戏

            Amazon -> Initialize(); //玩家操作
            Amazon -> ReCordLoad();
            repaint();

            if (!Amazon -> Judge()) { //游戏结束
                if (isRunning) {
                    QMessageBox :: information(this, tr("游戏结束"), tr("AI获胜"));

                    isRunning = false;
                    ui->recordButton->setVisible(false); //游戏结束时不可存档
                    ui -> replaceButton -> setVisible(false); //游戏结束时关闭AI辅助键
                }
                return;
            }

            isBeing = true, isAI = false; //接下来开启鼠标操作
            ui -> replaceButton -> raise();
            ui -> replaceButton -> setVisible(true);
        }
        else { //AI先手
            isAI = true, isBeing = false;
            AIplay(); //AI操作
        }

        return;
    });

    Amazon = new amazon();
    GameRunning();
}

MainWindow :: ~MainWindow()
{
    delete ui;
}

void MainWindow :: paintEvent(QPaintEvent *event) {

    static QPixmap table(":/pic/table.gif");
    static QPixmap arrow(":/pic/arrow.gif");
    static QPixmap goal(":/pic/goal.gif");
    static QPixmap black0(":/pic/black.gif");
    static QPixmap white0(":/pic/white.gif");
    static QPixmap empty0(":/pic/empty.gif");
    static QPixmap black1(":/pic/blackChosen.gif");
    static QPixmap white1(":/pic/whiteChosen.gif");
    static QPixmap empty1(":/pic/emptyChosen.gif");

    QPainter painter(this);
    painter.drawPixmap(QRectF(0, 0, 600, 600), table, table.rect());

    //str(25, 23) size 70 * 70
    for (int i = 0; i < 8; ++i)
        for (int j = 0; j < 8; ++j) {
            QRectF rec = QRectF(25 + i * 69.5, 23 + j * 70, 70, 70);

            if (!Amazon -> expected[i][j]) {
                if (Amazon -> map[i][j] == 0) {painter.drawPixmap(rec, empty0, empty0.rect()); continue; }
                if (Amazon -> map[i][j] == 1) {painter.drawPixmap(rec, black0, empty0.rect()); continue; }
                if (Amazon -> map[i][j] == -1) {painter.drawPixmap(rec, white0, empty0.rect()); continue; }
                if (Amazon -> map[i][j] == 2) {painter.drawPixmap(rec, arrow, empty0.rect()); continue; }
            }

            if (Amazon -> expected[i][j] == 1) {painter.drawPixmap(rec, goal, goal.rect()); continue; }

            //Amazon -> expected[i][j] == -1
            if (Amazon -> map[i][j] == 0) {painter.drawPixmap(rec, empty1, empty1.rect()); continue; }
            if (Amazon -> map[i][j] == 1) {painter.drawPixmap(rec, black1, empty1.rect()); continue; }
            if (Amazon -> map[i][j] == -1) {painter.drawPixmap(rec, white1, empty1.rect()); continue; }
        }

    return;
}

void MainWindow :: mousePressEvent(QMouseEvent *event) {
    if (!isBeing) return;

    qreal x = event -> x();
    qreal y = event -> y();
    int posX = ((double)x - 25) / 69.5, posY = ((double)y - 23) / 70; //点定位

    Amazon -> expect(posX, posY, stepCount);

    repaint(); //重绘界面
    if (stepCount == 3) { //玩家完成决策
        stepCount = 0;
        for (int i = 0; i < amazon :: N; ++i)
            for (int j = 0; j < amazon :: N; ++j) Amazon -> expected[i][j] = 0;

        Amazon -> ReCordRecord(), ++operateCount;
        ui -> recordButton -> setVisible(true);

        isBeing = false, isAI = true;
        AIplay(); //接下来AI操作
    }

    return;
}

void MainWindow :: AIplay() {//AI操作

    Amazon -> Initialize();
    Amazon -> ReCordLoad(); //载入棋局
    repaint();

    if (!Amazon -> Judge()) { //判断终局
        if (isRunning) {
            QMessageBox :: information(this, tr("消息框"), tr("游戏结束, 玩家获胜"));

            isRunning = false;
            ui -> recordButton -> setVisible(false); //游戏结束时不可存档
            ui -> replaceButton -> setVisible(false); //游戏结束时AI辅助键关掉
        }

        return;
    }

    ui -> nextButton -> raise();
    ui -> nextButton -> setVisible(true);

    if (operateCount) ui -> retryButton -> setVisible(true);
    //玩家可以选择让对方落子或重新落子

    return;
}


void MainWindow :: NewGame() { //新游戏

    switch(QMessageBox :: warning(this,tr("消息框"),
            tr("您将开启新游戏"),
            QMessageBox :: Ok|QMessageBox::Cancel,
            QMessageBox :: Ok))
        {
        case QMessageBox :: Ok:
            //次级键/标签要消失
            ui -> nextButton -> setVisible(false);
            ui -> retryButton -> setVisible(false);
            ui -> replaceButton -> setVisible(false);
            ui -> blackButton -> setVisible(false);
            ui -> whiteButton -> setVisible(false);
            ui -> askingColorLabel -> setVisible(false);
            ui -> showingLabel -> setVisible(false);
            ui -> blackButton2 -> setVisible(false);
            ui -> whiteButton2 -> setVisible(false);
            ui -> askingColorLabel2 -> setVisible(false);
            ui -> askingLevelLabel -> setVisible(false);
            ui -> Level0Button -> setVisible(false);
            ui -> Level1Button -> setVisible(false);
            ui -> Level2Button -> setVisible(false);
            ui -> replaceButton -> setVisible(false);

            stepCount = operateCount = 0;
            isAI = isBeing = isRunning = false;

            ui -> recordButton -> setVisible(false);

            Amazon -> Initialize();
            repaint();

            ui -> widget_3 -> raise();
            ui -> askingLevelLabel -> setVisible(true);
            ui -> Level0Button -> setVisible(true);
            ui -> Level1Button -> setVisible(true);
            ui -> Level2Button -> setVisible(true);

           break;
        case QMessageBox :: Cancel:
           break;
        default:
           break;
        }

    return;
}

void MainWindow :: Record() { //存档

    switch(QMessageBox :: warning(this,tr("消息框"),
            tr("是否存档？"),
            QMessageBox :: Ok|QMessageBox::Cancel,
            QMessageBox :: Ok))
        {
        case QMessageBox :: Ok:
           system("copy record.txt file.txt");
           break;
        case QMessageBox :: Cancel:
           break;
        default:
           break;
        }

    return;
}

void MainWindow :: LoadDoit() { //读档
    FILE* fp = fopen("file.txt", "r");
    fclose(fp);

    if (!fp) { //如果读不到档案, 返回
        QMessageBox :: information(this, tr("消息框"), tr("未读取到存档"));
        return;
    }

    //读档游戏

    //次级键/标签要消失
    ui -> nextButton -> setVisible(false);
    ui -> retryButton -> setVisible(false);
    ui -> replaceButton -> setVisible(false);
    ui -> blackButton -> setVisible(false);
    ui -> whiteButton -> setVisible(false);
    ui -> askingColorLabel -> setVisible(false);
    ui -> showingLabel -> setVisible(false);
    ui -> blackButton2 -> setVisible(false);
    ui -> whiteButton2 -> setVisible(false);
    ui -> askingColorLabel2 -> setVisible(false);
    ui -> askingLevelLabel -> setVisible(false);
    ui -> Level0Button -> setVisible(false);
    ui -> Level1Button -> setVisible(false);
    ui -> Level2Button -> setVisible(false);

    system("copy file.txt record.txt"); //读档

    stepCount = operateCount = 0;
    isAI = isBeing = isRunning = false;
    ui -> recordButton -> setVisible(false); //新读档的棋局不需要存档

    Amazon -> Initialize();
    Amazon -> ReCordLoad(); //加载棋局
    repaint();

    //接下来决定先后手
    if (Amazon -> curBotColor == 1) ui -> showingLabel -> setText("当前黑方执子");
    else  ui -> showingLabel -> setText("当前白方执子");
    ui -> showingLabel -> setVisible(true);
    ui -> askingColorLabel2 -> setVisible(true);
    ui -> blackButton2 -> setVisible(true);
    ui -> whiteButton2 -> setVisible(true);

    isAI = isBeing = false;

    return;
}

void MainWindow :: Load() { //读档

    switch(QMessageBox :: warning(this,tr("消息框"),
            tr("您将读档。"),
            QMessageBox :: Ok|QMessageBox::Cancel,
            QMessageBox :: Ok))
       {
       case QMessageBox :: Ok:
           LoadDoit();
           break;
       case QMessageBox::Cancel:
           return;
           break;
       default:
           break;
       }

    return;
}

void MainWindow :: Quit() { //退出

    if (isRunning && operateCount) { //如果棋局未到终局且玩家或AI操作过
        switch(QMessageBox :: warning(this,tr("消息框"),
                tr("当前棋局可能未保存, 是否存档？"),
                QMessageBox :: Save|QMessageBox::Discard|QMessageBox::Cancel,
                QMessageBox :: Save))
           {
           case QMessageBox :: Save:
               system("copy record.txt file.txt");
               close();
               break;
           case QMessageBox :: Discard:
               close();
               break;
           case QMessageBox :: Cancel:
               return;
               break;
           default:
               break;
           }
    }
    else {
        switch(QMessageBox :: warning(this,tr("消息框"),
                tr("您将退出游戏桌。"),
                QMessageBox :: Ok|QMessageBox::Cancel,
                QMessageBox :: Ok))
           {
           case QMessageBox :: Ok:
               close();
               break;
           case QMessageBox :: Cancel:
               return;
               break;
           default:
               break;
           }
    }

    return;
}

void MainWindow :: GameRunning() { //初始化

    stepCount = operateCount = 0;
    isAI = isBeing = isRunning = false;

    //功能键
    ui -> newGameButton -> setVisible(true);
    ui -> quitButton -> setVisible(true);
    ui -> recordButton -> setVisible(false); //初始时存档键不显示
    ui -> loadButton -> setVisible(true);

    //次级键/标签要消失
    ui -> nextButton -> setVisible(false);
    ui -> retryButton -> setVisible(false);
    ui -> replaceButton -> setVisible(false);
    ui -> blackButton -> setVisible(false);
    ui -> whiteButton -> setVisible(false);
    ui -> askingColorLabel -> setVisible(false);
    ui -> showingLabel -> setVisible(false);
    ui -> blackButton2 -> setVisible(false);
    ui -> whiteButton2 -> setVisible(false);
    ui -> askingColorLabel2 -> setVisible(false);
    ui -> askingLevelLabel -> setVisible(false);
    ui -> Level0Button -> setVisible(false);
    ui -> Level1Button -> setVisible(false);
    ui -> Level2Button -> setVisible(false);

    return;
}
