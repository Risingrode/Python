#ifndef AMAZON_H
#define AMAZON_H

#include <queue>
#include <cstdio>

typedef std :: pair <int, int> node;

class amazon{
public:
    const static int N = 8;
    const static int inf = 1e9;
    const static int TOTAL = 5e4 + 5;
    constexpr static double Ec = 0.08; //设置先手优势系数

    int Num[6], TurnCount, curBotColor, map[N][N], level;

    amazon();

    //博弈部分
    void Initialize ();
    bool Judge(); //判断执子
    void DecisionMaking();

    //存档记录部分
    int ReCordm, ReCordlen, ReCordlevel, ReCorda[100][6], ReCordflag;
    void ReCordInitialize ();
    void ReCordRecord();
    void ReCordWithDraw();
    void ReCordLoad();

    //输入部分
    int expected[N][N];
    void expect(const int &x, const int &y, int &stepCount);

private:
    std :: queue <node> que;
    FILE* fp;

    int gox[N] = {1, -1, -1, 0, 1, -1, 0, 1};
    int goy[N] = {0, 0, 1, 1, 1, -1, -1, -1};
    int vis[N][N], lst[N][N], total, mobility[N][N], id[TOTAL], stability[N][N], Tclock;

    double t1, t2, p1, p2, m; //评估值
    double value[TOTAL];
    bool stableFlag;

    node opt[TOTAL][3];

    int sgn(const int &x);
    bool CheckPosition(const int &x, const int &y);
    bool CheckAvailability(const node &s, const node &t);
    bool CheckOperation(const node &s, const node &t, const node &b, const int &id);
    bool ExecuteOperation(const node &s, const node &t, const node &b, const int &id);
    void WithDraw(const node &s, const node &t, const node &b, const int &id);


    //评估函数1.0  初级评估函数 int
    int Value1(const int &id);
    int Evaluate1();

    //评估函数2.0 评估值类型为double
    void check_stable(const int &id);
    void calc_mobility();
    double calcM(const int &id);
    void bfsQ(const int &id);
    void EvaluateQ();
    void bfsK(const int &id);
    void EvaluateK();
    //评估2.0
    double Evaluate2();

    //决策
    void DecisionMaking1();
    void DecisionMaking2();
    //决策3.0 双层遍历版本 估价函数稍更改, 双层搜索 + MinMax优化 + AlphaBeta剪枝
    //发现在决策很多的时候大概率超时, 解决方案: 在一层的时候评估一下
    bool MinEvaluate(double &MaxValue, const double &extra);
    void DecisionMaking3();

};

#endif // AMAZON_H
