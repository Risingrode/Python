import pycoin.key.Keychain as pk
from pycoin.key.Key import Key

# 生成私钥
private_key = Key.random()

# 生成公钥
public_key = private_key.public_copy()

# 生成 Testnet 地址
address = public_key.address(is_test=True)

# 检查地址是否有效

if is_address_valid(address):
    print("地址有效：", address)
else:
    print("地址无效！")
