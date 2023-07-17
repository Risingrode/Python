
import hashlib


msg=input("输入消息：")

dg=hashlib.sha256(msg.encode()).digest()

print(dg)











