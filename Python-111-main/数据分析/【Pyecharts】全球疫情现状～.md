### 前言[¶](#前言)

虽然国内疫情已经接近尾声，但从全球的数据来看，目前形式依然严峻；

全球确诊病例依然居高不下，自7月份以来，**每日新增确诊一直维持在20W-30W之间**，未见下降趋势；

截止9月10日，全球**累计确诊已达2800W例，死亡90W例**；

累计确诊病例超过100W的已有四个国家，分别是**美国（640W），印度（456W），巴西（424W）和俄罗斯（104W）**；

------

🗯 数据来源[🦠全球新冠肺炎COVID-19数据](https://www.kesci.com/home/dataset/5ea28f8d105d91002d4faebd);

🗣 可视化部分代码基于pyecharts V1.7.1，**使用基础镜像的同学请先执行`!pip install pyecharts==1.7.1`进行升级；**

------

📩  **欢迎订阅我的专栏[【🏝 数据之美】](https://www.kesci.com/home/column/5e5cef70704543002c985797)**；

📩  ~~**欢迎订阅我的新专栏[【🏝 决战潘大师】](https://www.kesci.com/home/column/5f49f25214f35900368b11f8)**,尽量会保持周更；~~

------

❗️ 为不影响阅读体验，我将代码隐藏了～

🏝 **需要代码的同学Fork之后在自己的Klab中【运行】，然后右上角选择【查看】-【隐藏/显示所有代码输入】就可以看到代码了**～

------

相关教程：

- ✨[【pyecharts】50个完整例子,带你玩转可视化～](https://www.kesci.com/mw/project/5faf844d7d1e6d0030d75665)
- ✨[**【pyecharts教程】应该是全网最全的教程了～**](https://www.kesci.com/home/project/5eb7958f366f4d002d783d4a)
- ✨[【Pyecharts Gallery】中看不中用的可视化作品集合～](https://www.kesci.com/home/project/5e4bd73f80da780037be6b61)

------

**🔴 广告位：**

- 🔥[LOL数据分析：英雄联盟2020春/夏季赛数据可视化～](https://www.kesci.com/mw/project/5f93926ee0eb3e003be0304c)
- 🔥[**【pyecharts】美国疫情数据&特朗普关于新冠的发言～**](https://www.kesci.com/mw/project/5fbbbcc6d3251d00303bba30)
- 🔥[ **【Pyecharts】🏆 湖人2019-20赛季投篮数据可视化~**](https://www.kesci.com/home/project/5f24d178d278b1002c23b323)
- 🔥[ 2021年最新世界大学排名，来看看你的母校上榜没～](https://www.kesci.com/home/project/5ef4246163975d002c8f3bbb)

------

### 现状[¶](#现状)

#### 累计确诊[¶](#累计确诊)

Out[5]:

#### 累计死亡[¶](#累计死亡)

Out[8]:

#### 累计治愈[¶](#累计治愈)

Out[11]:

#### 现状[¶](#现状)

Out[13]:

### 趋势[¶](#趋势)

#### 时间序列[¶](#时间序列)

Out[16]:

#### 每日新增趋势[¶](#每日新增趋势)

In [17]:

```
# 数据分别转为list，并将日期格式化为‘yyyy-MM-dd’格式
data_x, data_y_confirm_add, data_y_death_add, data_y_recover_add = [],[],[],[]
for idx in range(1, df_global.shape[0]):
    label = time.strftime("%Y-%m-%d",time.strptime(df_global.iloc[idx, 0], '%m/%d/%y'))
    data_x.append(label)
    data_y_confirm_add.append(int(df_global.iloc[idx, 1] - df_global.iloc[idx-1, 1]))
    data_y_death_add.append(int(df_global.iloc[idx, 2] - df_global.iloc[idx-1, 2]))
    data_y_recover_add.append(int(df_global.iloc[idx, 3] - df_global.iloc[idx-1, 3]))
```

Out[19]:

#### 新增TOP[¶](#新增TOP)

Out[20]:

- 🌈 ***欢迎点赞，Fork～～～\***  