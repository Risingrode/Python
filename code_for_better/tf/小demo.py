import tensorflow as tf
import numpy as np
from tensorflow import keras

# 创建尽可能最简单的神经网络。该神经网络有一个层，该层有一个神经元，其输入形状只有一个值。
model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
# 编写代码以编译神经网络。执行此操作时，您需要指定两个函数：loss 和 optimizer
model.compile(optimizer='sgd', loss='mean_squared_error')
# 提供数据
xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)
# 训练神经网络
model.fit(xs, ys, epochs=500)
# 使用模型预测
print(model.predict([10.0]))
