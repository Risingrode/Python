
'''
def _max(a ,b):
    print("最大数字是：",end=" ")
    if a>b:
        print(a)
    else:
        print(b)
    return

a=[1,2,3]
a="Runoob"

for x in a:
    print(x,end="")

def changeme(mylist):
    # "修改传入的列表"
    mylist.append([1, 2, 3, 4])
    print("函数内取值: ", mylist)
    return

# 调用changeme函数
mylist = [10, 20, 30]
changeme(mylist)
print("函数外取值: ", mylist)

print()         #这是一个换行语句
a=int(input("请输入第一个数字："))
b=int(input("请输入第二个数字："))

_max(a,b)

'''
