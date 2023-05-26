import os, binascii, hashlib, base58, ecdsa, requests


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


balance = 0
n = 0

while True:
    priv_key = os.urandom(32)
    fullkey = '80' + binascii.hexlify(priv_key).decode()
    sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
    sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
    WIF = base58.b58encode(binascii.unhexlify(fullkey + sha256b[:8]))
    sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
    hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
    publ_addr_a = b"\x00" + hash160
    checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
    publ_addr_b = base58.b58encode(publ_addr_a + checksum)
    # balance_url = "https://login.blockchain.com/en/#/recover" + publ_addr_b.decode()

    response = requests.get("https://sochain.com/api/v2/address/BTC/" + str(publ_addr_b.decode()))
    req = float(response.json()['data']['balance'])

    # req = requests.get(balance_url)
    balance += 1
    print("第{0}次搜索".format(balance)) # 下标需要从0开始判断

    if req != 0:
        print("Private Key : " + WIF.decode())
        print("Bitcoin Address: " + publ_addr_b.decode())
        input()


