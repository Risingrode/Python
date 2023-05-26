# 导入百度飞桨库


# 定义一个简单的线性网络
x = fluid.layers.data(name='x', shape=[1], dtype='float32')
y = fluid.layers.data(name='y', shape=[1], dtype='float32')
y_predict = fluid.layers.fc(input=x, size=1, act=None)

# 定义损失函数
cost = fluid.layers.square_error_cost(input=y_predict, label=y)
avg_cost = fluid.layers.mean(cost)

# 定义优化方法
optimizer = fluid.optimizer.SGDOptimizer(learning_rate=0.01)
opts = optimizer.minimize(avg_cost)

# 创建执行器，初始化参数
place = fluid.CPUPlace()
exe = fluid.Executor(place)
exe.run(fluid.default_startup_program())

# 训练100个批次
for i in range(100):
    outs = exe.run(
        feed={'x': train_data, 'y': true_data},
        fetch_list=[y_predict, avg_cost])
    print("第 %d 个批次，损失为：%s" % (i, outs[1][0]))