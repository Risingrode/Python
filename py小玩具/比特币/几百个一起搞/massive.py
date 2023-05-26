# massiveM.py Bitcoin Legacy compressed/uncompresses address. 04/07/2021
# Search for mnemonics 128 addresses from one 12 word mnemonics and balance checked
# Good Luck and Happy Hunting. Made by mizogg.co.uk
# Donations 3M6L77jC3jNejsd5ZU1CVpUVngrhanb6cD
from time import sleep
import itertools
import requests
import bitcoinlib
import random, os, hashlib
import atexit
from time import time
from datetime import timedelta, datetime
import csv
from itertools import zip_longest

def seconds_to_str(elapsed=None):
    if elapsed is None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        return str(timedelta(seconds=elapsed))


def log(txt, elapsed=None):
    print('\n '  + '  [TIMING]> [' + seconds_to_str() + '] ----> ' + txt + '\n')
    if elapsed:
        print("\n " + " [TIMING]> Elapsed time ==> " + elapsed + "\n" )


def end_log():
    end = time()
    elapsed = end - start
    log("End Program", seconds_to_str(elapsed))


start = time()
atexit.register(end_log)
log("Start Program")

print("massiveM.py. List loading Good Luck...")

filename = 'wordlist.txt'
with open(filename) as file:
    wordlist = file.read().split()


def create_valid_mnemonics(strength=128):
    rbytes = os.urandom(strength // 8)
    h = hashlib.sha256(rbytes).hexdigest()
    b = (bin(int.from_bytes(rbytes, byteorder="big"))[2:].zfill(len(rbytes) * 8) \
         + bin(int(h, 16))[2:].zfill(256)[: len(rbytes) * 8 // 32])
    result = []
    for i in range(len(b) // 11):
        idx = int(b[i * 11: (i + 1) * 11], 2)
        result.append(wordlist[idx])
    return " ".join(result)


def mnem_to_seed(words):
    salt = 'mnemonic'
    seed = hashlib.pbkdf2_hmac("sha512", words.encode("utf-8"), salt.encode("utf-8"), 2048)
    return seed


def seed_to_privatekey(seed):
    b = bitcoinlib.keys.HDKey.from_seed(seed)
    b0 = b.subkey_for_path("0")
    return b0.address()

query = []
count = 0
total = 0

while True:
    line = create_valid_mnemonics() # 助记词
    seed = mnem_to_seed(line)
    addr = seed_to_privatekey(seed)# 密钥
    count += 1
    try:
        request = requests.get("https://blockchain.info/multiaddr?active=%s" % ','.join(addr))
        request = request.json()
        print('Nihao')
        for row in request["addresses"]:
            print(row)
            if row["total_received"] > 0 or row["final_balance"] > 0:  # final_balance or n_tx or total_received or total_sent
                    print('找到一个')
                    f = open(u"winner.txt", "a")
                    f.write('\n' +  "0" + '      Bitcoin Address : ' + addr)
                    f.close()
                    break
    except:
        pass
    query = []
