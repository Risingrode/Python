from pymouse import PyMouse ##鼠标
from pykeyboard import PyKeyboard ##键盘

import time
import sys
m = PyMouse() ##鼠标实例
k = PyKeyboard() ##键盘实例
print('请输入需要控制位置的横纵分辨率')
w = input()
h = input()
with open('out.txt','r') as f:
    for line in f.readlines():
        line=line.strip('\n')
        m.click(int(w), int(h))
        k.type_string(line)
        sys.stdout.flush()
        time.sleep(3)
        k.tap_key(k.enter_key)

'''     
try:
    while 1:
        m.click(int(w), int(h))
        k.type_string('xxx')
        sys.stdout.flush()
        time.sleep(3)
        k.tap_key(k.enter_key)
except KeyboardInterrupt:
    print("捕获异常")
'''
