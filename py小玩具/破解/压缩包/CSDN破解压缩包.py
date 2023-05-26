import zipfile
import itertools
import math

dictionaries = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V', 'W', 'X', 'Y', 'Z',
                '.', ',', ':', '?', '<', '>',
                ' ']  # 组成破解字典的关键字符（可以按照自己需求添加）
diction_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
diction_upp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
diction_low = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']


def allkeyword(number):  # 排列出字符所有number个字符的组合
    allkey1 = itertools.product(dictionaries, repeat=number)
    allkey2 = (''.join(i) for i in allkey1)
    return allkey2


def trypassword(fileName, password):  # 用trypassword函数返回的True或者Flase来判定程序是否终止。
    try:
        ZIPFILE = zipfile.ZipFile(fileName)  # 定义对象，相当于定义一个压缩文件1.zip
        ZIPFILE.extractall(path='./', pwd=password.encode('utf-8'))
        print(f"解压成功,正确密码为：{password}")
        return True
    except:
        return False


def start(fileName):
    print("是否有确定长度，输入0是否，其它数字为长度:")
    Lenth = input()
    if Lenth != 0:
        print("输入1为纯数字，输入2为纯大写，输入3为纯小写，输入4数字加大写，输入5数字加小写，输入6大写加小写:")
        num = input()
        if num == 1:
            num_arr = itertools.product(diction_num, repeat=Lenth)
            num_list = (''.join(i) for i in num_arr)
            for pwd in num_list:
                if trypassword(fileName, pwd):  # 判断结果是否正确
                    return
                else:
                    pass
        elif num == 3:
            low_arr = itertools.product(diction_low, repeat=Lenth)
            low_list = (''.join(i) for i in low_arr)
            print(low_list)
            for pwd in low_list:
                if trypassword(fileName, pwd):  # 判断结果是否正确
                    return
                else:
                    pass
        else:
            print('有空再写')
    else:
        for number in range(20):  # 遍历长度在20以内的所有可能密码组合
            print("密码长度：", number + 1)
            index = 0
            for pwd in allkeyword(number + 1):
                index = index + 1
                print("进度:", str(round(100 * index / (Lenth(dictionaries) ** (number + 1)), 2)) + "%", end="\r")
                if trypassword(fileName, pwd):  # 判断结果是否正确
                    return


start("Bitcoin.zip")
