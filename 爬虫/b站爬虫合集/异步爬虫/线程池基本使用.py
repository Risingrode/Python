# import time
#
# def get_page(str):
#     print("正在下载：",str)
#     time.sleep(2)
#     print("下载成功：",str)
#
# name_str=['xiaokeai','xiaoming','dabao']
# start_time=time.time()
# for i in range(len(name_str)):
#     get_page(name_str[i])
# end_time=time.time()
# print('%d second'%(end_time-start_time))


# 使用线程池
import time
# 导入线程池
from multiprocessing.dummy import Pool

start_time = time.time()

def get_page(str):
    print("正在下载：", str)
    time.sleep(2)
    print("下载成功：", str)

name_str = ['xiaokeai', 'xiaoming', 'dabao', 'xiaohua']

pool = Pool(4)  # 在池子中开辟4个对象空间
# 把列表中的每一个元素添加到函数中
# 如果get_page有返回值  map会有返回值

pool.map(get_page, name_str)  # 发生阻塞的操作
end_time = time.time()
print('总时间是：', end_time - start_time)









