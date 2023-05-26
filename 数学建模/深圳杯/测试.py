import numpy
import pandas

from spsspro.algorithm import statistical_model_analysis
#生成案例数据
data_x1 = pandas.DataFrame({
    "A": numpy.random.random(size=100),
    "B": numpy.random.random(size=100)
})
data_x2 = pandas.DataFrame({"C": numpy.random.choice(["1", "2", "3"], size=100)})
data_y = pandas.Series(data=numpy.random.choice([1, 2], size=100), name="Y")
#线性回归，输入参数详细可以光标放置函数括号内按shift+tab查看，输出结果参考spsspro模板分析报告
result = statistical_model_analysis.linear_regression(data_y=data_y, data_x1=data_x1, data_x2=data_x2)
print(result)