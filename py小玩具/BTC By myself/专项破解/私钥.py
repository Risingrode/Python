

# TODO：这个找到该地址下的余额，好用


import multiprocessing
from multiprocessing import Process, Queue
from multiprocessing.pool import ThreadPool
import base58
import ecdsa  # 椭圆加密算法
import requests
from bitcoin import *
import random

# 单词列表
wordlist = []

# 产生私钥
def generate_private_key():
    low = 0x1  # starting point
    high = 0x10000  # ending point

    while True:
        ran = random.randrange(low, high, 1)

        myhex = "%064x" % ran
        myhex = myhex[:64]
        private_key = myhex
        return private_key


# 这里是把私钥转化成WIF
def private_key_to_WIF(private_key):
    var80 = "80" + str(private_key)
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')


# 私钥产生公钥
def private_key_to_public_key(private_key):
    sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve=ecdsa.SECP256k1)
    return ('04' + binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8'))


# 公钥产生地址
def public_key_to_address(public_key):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    count = 0
    val = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    doublehash = hashlib.sha256(
        hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()
    address = '00' + var.hexdigest() + doublehash[0:8]
    for char in address:
        if (char != '0'):
            break
        count += 1
    count = count // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    while (val < count):
        output.append(alphabet[0])
        val += 1
    return ''.join(output[::-1])


# 导入一个地址，获取该地址里的钱数
def get_balance(address):
    try:
        response = requests.get("https://sochain.com/api/v2/address/BTC/" + str(address))
        return float(response.json()['data']['balance'])
    except:
        return -1


def data_export(queue):
    while True:
        private_key = generate_private_key()
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)
        data = (private_key, address)
        queue.put(data, block=False)


# 无限循环 多线程就是跑这个函数
def worker(queue):
    while True:
        if not queue.empty():
            data = queue.get(block=True)  # 获取数据
            balance = get_balance(data[1])  # 获取钱数
            process(data, balance)


# 进行判断是否有钱，输出最终结果
def process(data, balance):
    private_key = data[0]
    address = data[1]
    if balance == -1:
        print("地址{:<34}".format(str(address)) + " : " + str(balance)+":"+private_key)
    if balance > 0.00000000:
        print('找到')
        file = open("found.txt", "a")
        file.write("address: " + str(address) + "\n" +
                   "private key: " + str(private_key) + "\n" +
                   "WIF private key: " + str(private_key_to_WIF(private_key)) + "\n" +
                   "public key: " + str(private_key_to_public_key(private_key)).upper() + "\n" +
                   "balance: " + str(balance) + "\n\n")
        file.close()


def thread(iterator):
    processes = []
    data = Queue()
    data_factory = Process(target=data_export, args=(data,))
    data_factory.daemon = True
    processes.append(data_factory)
    data_factory.start()
    work = Process(target=worker, args=(data,))
    work.daemon = True
    processes.append(work)
    work.start()
    data_factory.join()


if __name__ == '__main__':
    try:
        pool = ThreadPool(processes=multiprocessing.cpu_count() * 6)
        pool.map(thread, range(0, 8))  # Limit to single CPU thread as we can only query 300 addresses per minute
    except:
        pool.close()
        exit()
