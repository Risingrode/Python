#include "amazon.h"
#include "mainwindow.h"
#include <cmath>
#include <ctime>
#include <cstdio>
#include <iostream>
#include <algorithm>

amazon :: amazon () {
    Initialize();
}

void amazon :: Initialize () { //初始化棋盘
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) map[i][j] = 0;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) expected[i][j] = 0;

    map[0][2] = map[2][0] = map[5][0] = map[7][2] = 1;
    map[0][5] = map[2][7] = map[5][7] = map[7][5] = -1;
    TurnCount = 0, curBotColor = -1;
}

int amazon :: sgn(const int &x) {
    if (!x) return 0;
    return x < 0 ? -1 : 1;
}

bool amazon :: CheckPosition(const int &x, const int &y) {
    if (x < 0 || x >= N) return false;
    if (y < 0 || y >= N) return false;
    return true;
}

//一些基础操作
#define sx s.first
#define sy s.second
#define tx t.first
#define ty t.second
#define bx b.first
#define by b.second

bool amazon :: CheckAvailability(const node &s, const node &t) { //s,t在棋盘上，s -> t路径上无棋子或障碍(不包括s,t位置)
    if (!CheckPosition(sx, sy) || !CheckPosition(tx, ty)) return false;

    int dx = sgn(tx - sx), dy = sgn(ty - sy), nx = sx, ny = sy;
    for (int i = 1; i; ++i) {
        nx += dx, ny += dy;
        if (!CheckPosition(nx, ny)) return false;
        if (nx == tx && ny == ty) return true;
        if (map[nx][ny]) return false;
    }

    return false; //这行实际上不会用到, 仅仅为了程序的规范性
}

bool amazon :: CheckOperation(const node &s, const node &t, const node &b, const int &id) { //判断操作是否合理
    if (!CheckPosition(sx, sy) || map[sx][sy] != id) return false;
    if (!CheckPosition(tx, ty) || map[tx][ty]) return false;
    if (!CheckPosition(bx, by)) return false;
    if (map[bx][by] && (bx != sx || by != sy)) return false;
    map[sx][sy] = 0;	//注意起始位置在目标位置和障碍位置连线上的情况
    bool flag = CheckAvailability(s, t) && CheckAvailability(t, b);
    map[sx][sy] = id;
    return flag;
}

bool amazon :: ExecuteOperation(const node &s, const node &t, const node &b, const int &id) { //执行一次操作
    if (CheckOperation(s, t, b, id)) return map[tx][ty] = map[sx][sy], map[sx][sy] = 0, map[bx][by] = 2, true;
    return false;
}

void amazon :: WithDraw(const node &s, const node &t, const node &b, const int &id) {
    map[bx][by] = 0, map[sx][sy] = map[tx][ty], map[tx][ty] = 0;
}

#undef sx
#undef sy
#undef tx
#undef ty
#undef bx
#undef by

//判断执子方能否走步
bool amazon :: Judge() {
    total = 0;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (map[i][j] == curBotColor) {
            int x = i, y = j;
            for (int k = 0; k < 8; ++k) {
                int nx = x, ny = y;
                for (int ki = 1; ; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny) || map[nx][ny]) break;
                    for (int l = 0; l < 8; ++l) {
                        int wx = nx, wy = ny;
                        for (int li = 1; ; ++li) {
                            wx += gox[l], wy += goy[l];
                            if (!CheckPosition(wx, wy)) break;
                            if (map[wx][wy] && (wx != x || wy != y)) break;

                            return true;
                        }
                    }
                }
            }
        }

    return false;
}

//评估函数1.0  初级评估函数 int
int amazon :: Value1(const int &id) {
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) vis[i][j] = 0;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (map[i][j] == id) {
            for (int k = 0; k < 8; ++k) {
                int nx = i, ny = j;
                for (int ki = 1; ki; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny)) break;
                    if (map[nx][ny]) break;

                    vis[nx][ny] = 1;
                }
            }
        }

    int cnt = 0;
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) cnt += vis[i][j];
    return cnt;
}

int amazon :: Evaluate1() {
    return Value1(curBotColor) - Value1(-curBotColor);
}

//评估函数2.0 评估值类型为double
void amazon :: check_stable(const int &id) {
    for (int x = 0; x < N; ++x)
        for (int y = 0; y < N; ++y) if (map[x][y] == id) {
            stability[x][y] = true;

            for (int i = 0; i < N; ++i)
                for (int j = 0; j < N; ++j) vis[i][j] = 0;

            while (!que.empty()) que.pop();
            vis[x][y] = 1, que.push(std :: make_pair(x, y));

            while (!que.empty()) {
                node cur = que.front(); que.pop();
                int cx = cur.first, cy = cur.second;
                for (int k = 0; k < 8; ++k) {
                    int nx = cx + gox[k], ny = cy + goy[k];
                    if (!CheckPosition(nx, ny)) continue;

                    if (vis[nx][ny]) continue;
                    vis[nx][ny] = 1;

                    if (map[nx][ny] == -id) stability[x][y] = false;
                    if (map[nx][ny]) continue;

                    que.push(std :: make_pair(nx, ny));
                }
            }
        }

    return;
}

void amazon :: calc_mobility() {
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) {
            mobility[i][j] = 0;
            for (int k = 0; k < 8; ++k) {
                int nx = i + gox[k], ny = j + goy[k];
                if (!CheckPosition(nx, ny) || map[nx][ny]) continue;
                ++mobility[i][j];
            }
        }

    return;
}

double amazon :: calcM(const int &id) {
    double res = 0, mn = inf;
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (map[i][j] == id) {
            for (int k = 0; k < 8; ++k) {
                int nx = i, ny = j;
                for (int ki = 1; ki; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny)) break;
                    if (map[nx][ny]) break;

                    res += (double)mobility[nx][ny] / (double)ki;
                    mn = std :: min(mn, (double)mobility[nx][ny] / (double)ki);
                }
            }
        }

    return res + mn;
}

void amazon :: bfsQ(const int &id) {
    while (!que.empty()) que.pop();
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) vis[i][j] = 1e9;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            if (map[i][j] == id)
                vis[i][j] = 0, que.push(std :: make_pair(i, j));

    while (!que.empty()) {
        node cur = que.front(); que.pop();
        int x = cur.first, y = cur.second;
        for (int k = 0; k < 8; ++k) {
            int nx = x, ny = y;
            for (int ki = 1; ki; ++ki) {
                nx += gox[k], ny += goy[k];
                if (!CheckPosition(nx, ny)) break;
                if (map[nx][ny]) break;
                if (vis[nx][ny] <= vis[x][y] + 1) continue;

                vis[nx][ny] = vis[x][y] + 1;
                que.push(std :: make_pair(nx, ny));
            }
        }
    }

    return;
}

void amazon :: EvaluateQ() {
    t1 = 0, p1 = 0;

    bfsQ(curBotColor);
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) lst[i][j] = vis[i][j];

    bfsQ(-curBotColor);

    stableFlag = true;
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (!map[i][j]) {
            if (vis[i][j] == lst[i][j]) t1 += Ec;
            else
                if (vis[i][j] > lst[i][j]) t1 += 1.0;
                else t1 -= 1.0;

            if (vis[i][j] < inf && lst[i][j] < inf) stableFlag = false;

            p1 += 2.0 * (pow(2.0, -lst[i][j]) - pow(2.0, -vis[i][j]));
        }
    return;
}

void amazon :: bfsK(const int &id) {
    while (!que.empty()) que.pop();
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) vis[i][j] = 1e9;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            if (map[i][j] == id)
                vis[i][j] = 0, que.push(std :: make_pair(i, j));

    while (!que.empty()) {
        node cur = que.front(); que.pop();
        int x = cur.first, y = cur.second;
        for (int k = 0; k < 8; ++k) {
            int nx = x + gox[k], ny = y + goy[k];
            if (!CheckPosition(nx, ny)) continue;
            if (map[nx][ny]) continue;
            if (vis[nx][ny] <= vis[x][y] + 1) continue;

            vis[nx][ny] = vis[x][y] + 1;
            que.push(std :: make_pair(nx, ny));
        }
    }

    return;
}

void amazon :: EvaluateK() {
    t2 = 0, p2 = 0;

    bfsK(curBotColor);
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) lst[i][j] = vis[i][j];

    bfsK(-curBotColor);
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (!map[i][j]) {
            if (vis[i][j] == lst[i][j]) t2 += Ec;
            else
                if (vis[i][j] > lst[i][j]) t2 += 1.0;
                else t2 -= 1.0;

            p2 += std :: min(1.0, std :: max(-1.0, ((double)vis[i][j] - lst[i][j]) / 6.0));
        }
    return;
}

//评估2.0
double amazon :: Evaluate2() {
    calc_mobility();
    m = (calcM(curBotColor) - calcM(-curBotColor)) / 30;

    EvaluateQ();
    EvaluateK();

    if (stableFlag) return t1;
    if (TurnCount < 10) return 0.14 * t1 + 0.37 * t2 + 0.13 * p1 + 0.13 * p2 + 0.20 * m;
    if (TurnCount < 25) return 0.30 * t1 + 0.25 * t2 + 0.20 * p1 + 0.20 * p2 + 0.05 * m;
    return 0.80 * t1 + 0.10 * t2 + 0.05 * p1 + 0.05 * p2;
}


//决策1.0 随机版本 目标:能够在规定时间内正常输出的随机Bot
void amazon :: DecisionMaking1() { //这里枚举了所有可能的下法，以便之后随机
    total = 0;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (map[i][j] == curBotColor) {
            int x = i, y = j;
            for (int k = 0; k < 8; ++k) {
                int nx = x, ny = y;
                for (int ki = 1; ; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny) || map[nx][ny]) break;
                    for (int l = 0; l < 8; ++l) {
                        int wx = nx, wy = ny;
                        for (int li = 1; ; ++li) {
                            wx += gox[l], wy += goy[l];
                            if (!CheckPosition(wx, wy)) break;
                            if (map[wx][wy] && (wx != x || wy != y)) break;

                            opt[total][0] = std :: make_pair(x, y);
                            opt[total][1] = std :: make_pair(nx, ny);
                            opt[total][2] = std :: make_pair(wx, wy);
                            ++total;
                        }
                    }
                }
            }
        }


    if (!total) { //本机操作中, 这种情况不会出现
        for (int i = 0; i < 6; ++i) std :: cout << -1 << ' ';
        putchar('\n');
        return;
    }

    std :: srand(time(NULL));
    int K = rand() % total;

    /*简单交互输出
    for (int i = 0; i < 3; ++i)
        printf("%d %d ", opt[K][i].first, opt[K][i].second);*/

    // 本机操作中不需要输出AI指令 只需记录
    for(int i = 0; i < 3; ++i)
        Num[i * 2] = opt[K][i].first, Num[i * 2 + 1] = opt[K][i].second;

    return;
}


//决策2.0 单层遍历版本 简单估价使它跑过随机
void amazon :: DecisionMaking2() {
    total = 0;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (map[i][j] == curBotColor) {
            int x = i, y = j;
            for (int k = 0; k < 8; ++k) {
                int nx = x, ny = y;
                for (int ki = 1; ; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny) || map[nx][ny]) break;
                    for (int l = 0; l < 8; ++l) {
                        int wx = nx, wy = ny;
                        for (int li = 1; ; ++li) {
                            wx += gox[l], wy += goy[l];
                            if (!CheckPosition(wx, wy)) break;
                            if (map[wx][wy] && (wx != x || wy != y)) break;

                            opt[total][0] = std :: make_pair(x, y);
                            opt[total][1] = std :: make_pair(nx, ny);
                            opt[total][2] = std :: make_pair(wx, wy);
                            ++total;
                        }
                    }
                }
            }
        }

    if (!total) { //本机操作中, 这种情况不会出现
        for (int i = 0; i < 6; ++i) std :: cout << -1 << ' ';
        putchar('\n');
        return;
    }

    int MaxValue = -inf, MaxID = -1;
    for (int i = 0; i < total; ++i) {
        ExecuteOperation(opt[i][0], opt[i][1], opt[i][2], curBotColor);
        int res = Evaluate1();
        if (res > MaxValue) MaxValue = res, MaxID = i;
        WithDraw(opt[i][0], opt[i][1], opt[i][2], curBotColor);
    }

    if (~MaxID) {
        /*简单交互输出
        for (int i = 0; i < 3; ++i)
            printf("%d %d ", opt[MaxID][i].first, opt[MaxID][i].second);*/

        // 本机操作中不需要输出AI指令 只需记录
        for(int i = 0; i < 3; ++i)
            Num[i * 2] = opt[MaxID][i].first, Num[i * 2 + 1] = opt[MaxID][i].second;
    }
    else { //本机操作中, 这种情况不会出现
        for (int i = 0; i < 6; ++i) std :: cout << -1 << ' ';
        putchar('\n');
    }

    return;
}

//决策3.0 双层遍历版本 估价函数稍更改, 双层搜索 + MinMax优化 + AlphaBeta剪枝
//发现在决策很多的时候大概率超时, 解决方案: 在一层的时候评估一下
bool amazon :: MinEvaluate(double &MaxValue, const double &extra) { //二层搜索
    double mn = inf;

    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (map[i][j] == -curBotColor) {
            int x = i, y = j;
            for (int k = 0; k < 8; ++k) {
                int nx = x, ny = y;
                for (int ki = 1; ; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny) || map[nx][ny]) break;
                    for (int l = 0; l < 8; ++l) {
                        int wx = nx, wy = ny;
                        for (int li = 1; ; ++li) {
                            wx += gox[l], wy += goy[l];
                            if (!CheckPosition(wx, wy)) break;
                            if (map[wx][wy] && (wx != x || wy != y)) break;

                            ExecuteOperation(std :: make_pair(x, y), std :: make_pair(nx, ny), std :: make_pair(wx, wy), -curBotColor);
                            double res = Evaluate2() + extra;
                            WithDraw(std :: make_pair(x, y), std :: make_pair(nx, ny), std :: make_pair(wx, wy), -curBotColor);

                            if (res <= MaxValue) return false;
                            mn = std :: min(res, mn);
                        }
                    }
                }
            }
        }

    if (mn == inf) {
        mn = Evaluate2() + extra + 1e5; //一个胜利的方案应该是优先考虑的方案, 同时有多个胜利方案时考虑权值最大的
        if (mn <= MaxValue) return false;
    }

    MaxValue = mn;

    return true;
}

void amazon :: DecisionMaking3() {
    total = 0;
    Tclock = clock();

    check_stable(curBotColor);
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j) if (map[i][j] == curBotColor) {
            int x = i, y = j;
            for (int k = 0; k < 8; ++k) {
                int nx = x, ny = y;
                for (int ki = 1; ; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny) || map[nx][ny]) break;
                    for (int l = 0; l < 8; ++l) {
                        int wx = nx, wy = ny;
                        for (int li = 1; ; ++li) {
                            wx += gox[l], wy += goy[l];
                            if (!CheckPosition(wx, wy)) break;
                            if (map[wx][wy] && (wx != x || wy != y)) break;

                            opt[total][0] = std :: make_pair(x, y);
                            opt[total][1] = std :: make_pair(nx, ny);
                            opt[total][2] = std :: make_pair(wx, wy);

                            ExecuteOperation(opt[total][0], opt[total][1], opt[total][2], curBotColor);
                            value[total] = Evaluate2() + (stability[i][j] ? 0 : 100), id[total] = total;
                            WithDraw(opt[total][0], opt[total][1], opt[total][2], curBotColor);

                            ++total;
                        }
                    }
                }
            }
        }

    if (!total) { //本机操作中, 这种情况不会出现
        for (int i = 0; i < 6; ++i) std :: cout << -1 << ' ';
        putchar('\n');
        return;
    }

    std :: sort(id, id + total, [&](int a, int b){
        return value[a] > value[b];
    });

    double MaxValue = -inf;
    int MaxID = 0;

    int checkpoint = 50;
    for (int k = 0, i; i = id[k], k < total; ++k) {
        ExecuteOperation(opt[i][0], opt[i][1], opt[i][2], curBotColor);
        if (MinEvaluate(MaxValue, (stability[opt[i][0].first][opt[i][0].second] ? 0 : 100))) MaxID = i;
        WithDraw(opt[i][0], opt[i][1], opt[i][2], curBotColor);
        if (k == checkpoint) {
            checkpoint += 20;
            if (clock() - Tclock > 500) break;
        }
    }

    if (~MaxID) {
        //简单交互输出
        /*for (int i = 0; i < 3; ++i)
            printf("%d %d ", opt[MaxID][i].first, opt[MaxID][i].second);*/

        //本机操作中不需要输出AI指令 只需记录
        for(int i = 0; i < 3; ++i)
            Num[i * 2] = opt[MaxID][i].first, Num[i * 2 + 1] = opt[MaxID][i].second;
    }
    else { //本机操作中, 这种情况不会出现
        for (int i = 0; i < 6; ++i) std :: cout << -1 << ' ';
        putchar('\n');
    }

    return;
}

void amazon :: DecisionMaking() {
    std :: cerr << level << std :: endl; //用于检验bot的等级
    if (level == 0) DecisionMaking1();
    else
        if (level == 1) DecisionMaking2();
        else DecisionMaking3();
    return;
}

//记录部分
void amazon :: ReCordInitialize () { //初始化记录文档
    fp = fopen("record.txt", "w");

    fprintf(fp, "1 %d\n-1 -1 -1 -1 -1 -1\n", level);

    fclose(fp);
    return;
}

void amazon :: ReCordRecord() {
    fp = fopen("record.txt", "r");

    fscanf(fp, "%d%d", &ReCordm, &ReCordlevel); ReCordlen = 0; ReCordflag = false;
    for (int i = 0; i < ReCordm; i++) {
        for (int k = 0; k < 6; ++k) fscanf(fp, "%d", &ReCorda[ReCordlen][k]);
        if(ReCorda[ReCordlen][0] >= 0) ReCordlen++; else ReCordflag = true;

        if (i < ReCordm - 1) {
            for (int k = 0; k < 6; ++k) fscanf(fp, "%d", &ReCorda[ReCordlen][k]);
            ReCordlen++;
        }
    }

    fclose(fp);

    for (int k = 0; k < 6; ++k) ReCorda[ReCordlen][k] = Num[k];
    ++ReCordlen;

    if (!ReCordflag) ++ReCordm;

    fp = fopen("record.txt", "w");

    fprintf(fp, "%d %d\n", ReCordm, ReCordlevel);
    if (!ReCordflag && ReCordm != 1) fprintf(fp, "-1 -1 -1 -1 -1 -1\n");
    for (int i = 0; i < ReCordlen; ++i)
        for (int k = 0; k < 6; ++k) fprintf(fp, "%d%c", ReCorda[i][k], " \n"[k == 5]);

    fclose(fp);

    return;
}

void amazon :: ReCordWithDraw() {
    fp = fopen("record.txt", "r");

    fscanf(fp, "%d%d", &ReCordm, &ReCordlevel); ReCordlen = 0; ReCordflag = false;
    for (int i = 0; i < ReCordm; i++) {
        for (int k = 0; k < 6; ++k) fscanf(fp, "%d", &ReCorda[ReCordlen][k]);
        if(ReCorda[ReCordlen][0] >= 0) ReCordlen++; else ReCordflag = true;

        if (i < ReCordm - 1) {
            for (int k = 0; k < 6; ++k) fscanf(fp, "%d", &ReCorda[ReCordlen][k]);
            ReCordlen++;
        }
    }

    fclose(fp);

    --ReCordlen;
    if (ReCordflag) --ReCordm;

    fp = fopen("record.txt", "w");

    fprintf(fp, "%d %d\n", ReCordm, ReCordlevel);
    if (!ReCordflag) fprintf(fp, "-1 -1 -1 -1 -1 -1\n");
    for (int i = 0; i < ReCordlen; ++i)
        for (int k = 0; k < 6; ++k) fprintf(fp, "%d%c", ReCorda[i][k], " \n"[k == 5]);

    fclose(fp);

    return;
}

void amazon :: ReCordLoad() { //载入数据 sample改
    fp = fopen("record.txt", "r");

    if (!fp) { //没有存档文件时, 新建一个空档
        fclose(fp);
        ReCordInitialize (); //初始化记录文档
        fp = fopen("record.txt", "r");
    }

    //读入到当前回合为止，自己和对手的所有行动，从而把局面恢复到当前回合
    fscanf(fp, "%d%d", &TurnCount, &level);
    ReCordm = TurnCount, ReCordlevel = level;

    curBotColor = -1; // 先假设自己是白子
    for (int i = 0; i < TurnCount; i++) {
        int x0, y0, x1, y1, x2, y2;
        fscanf(fp, "%d%d%d%d%d%d", &x0, &y0, &x1, &y1, &x2, &y2);

        // 首先是对手行动
        if (x0 == -1) curBotColor = 1; //第一回合收到坐标是-1, -1，说明我是黑方
        else ExecuteOperation(std :: make_pair(x0, y0), std :: make_pair(x1, y1), std :: make_pair(x2, y2), -curBotColor); //模拟对方落子

        // 然后是自己当时的行动
        // 对手行动总比自己行动多一个
        if (i < TurnCount - 1) {
            fscanf(fp, "%d%d%d%d%d%d", &x0, &y0, &x1, &y1, &x2, &y2);
            if (x0 >= 0) ExecuteOperation(std :: make_pair(x0, y0), std :: make_pair(x1, y1), std :: make_pair(x2, y2), curBotColor); // 模拟己方落子
        }
    }
    if (TurnCount == 0) curBotColor = 1;

    fclose(fp);

    return;
}


void amazon :: expect(const int &x, const int &y, int &stepCount) {
    if (x < 0 || x >= N) return;
    if (y < 0 || y >= N) return;
    if (map[x][y] != curBotColor && expected[x][y] != 1) return;

    if (expected[x][y] != 1) {

        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j) expected[i][j] = 0;
        expected[x][y] = -1;
        Num[0] = x, Num[1] = y;

        for (int k = 0; k < 8; ++k) {
            int nx = x, ny = y;
            for (int ki = 1; ; ++ki) {
                nx += gox[k], ny += goy[k];
                if (!CheckPosition(nx, ny) || map[nx][ny]) break;
                expected[nx][ny] = 1;
            }
        }

        stepCount = 1;
    }
    else
        if (stepCount == 1) {

            for (int i = 0; i < N; ++i)
                for (int j = 0; j < N; ++j) expected[i][j] = 0;
            expected[Num[0]][Num[1]] = -1, expected[x][y] = -1;
            Num[2] = x, Num[3] = y;

            map[Num[0]][Num[1]] = 0;
            for (int k = 0; k < 8; ++k) {
                int nx = x, ny = y;
                for (int ki = 1; ; ++ki) {
                    nx += gox[k], ny += goy[k];
                    if (!CheckPosition(nx, ny) || map[nx][ny]) break;
                    expected[nx][ny] = 1;
                }
            }
            map[Num[0]][Num[1]] = curBotColor;

            stepCount = 2;
        }
        else {
            for (int i = 0; i < N; ++i)
                for (int j = 0; j < N; ++j) expected[i][j] = 0;
            Num[4] = x, Num[5] = y;

            stepCount = 3;
        }

    return;
}
