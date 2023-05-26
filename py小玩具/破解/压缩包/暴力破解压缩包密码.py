import zipfile
import itertools

filename = '国赛建模.zip'
lowercase_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
a = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
b = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
     'X', 'Y', 'Z']
Path = 'Bitcoin.zip'


def uncompress(filename, password):
    try:
        with zipfile.ZipFile(Path) as zfile:
            zfile.extractall("./", pwd=password.encode('utf-8'))
        return True
    except:
        return False


if __name__ == '__main__':
    dic_list = itertools.product(a, repeat=4)
    di_list = itertools.product(b, repeat=1)
    for n in b:
        for m in b:
            for i in dic_list:
                password = n + m + ''.join(i)
                result = uncompress(filename, password)
                if (result):
                    print('密码是：' + password)
                    input('成功')
                else:
                    print('执行中' + password)

'''
Python有个pyzipper库可以很好的兼容代替zipfile，可以读写AES加密的zip文件
f1 = open('D:\python\passdict4.txt','r')
with pyzipper.AESZipFile(file_path,'r') as f:
   for i in f1:
       i = i.rstrip('\n')
       f.pwd = str.encode(i)
       try:
           f.extractall(path=f"{root}")
           print(file_path+"\t密码是:"+i)
           break
       except Exception:
           pass
f.close()
f1.close()
'''
