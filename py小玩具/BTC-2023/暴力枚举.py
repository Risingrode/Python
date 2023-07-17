import os
import threading
from web3 import Web3

# Establish connection to an Ethereum node
ether = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com'))
bsc   = Web3(Web3.HTTPProvider('https://bsc.publicnode.com'))
arb   = Web3(Web3.HTTPProvider('https://arbitrum-one.publicnode.com'))
matic = Web3(Web3.HTTPProvider('https://polygon-bor.publicnode.com'))
avax  = Web3(Web3.HTTPProvider('https://avalanche-c-chain.publicnode.com'))
ftm   = Web3(Web3.HTTPProvider('https://fantom.publicnode.com'))
opt   = Web3(Web3.HTTPProvider('https://optimism.publicnode.com'))

def check_private_key(private_key):
    # Convert the private key to an account address
    account = ether.eth.account.from_key(private_key)
    address = account.address

    # Get the balance of addresses
    ethbalance = ether.eth.get_balance(address)
    bscbalance = bsc.eth.get_balance(address)
    arbbalance = arb.eth.get_balance(address)
    mtcbalance = matic.eth.get_balance(address)
    avxbalance = avax.eth.get_balance(address)
    ftmbalance = ftm.eth.get_balance(address)
    optbalance = opt.eth.get_balance(address)

    if ethbalance > 0:
        output = f'Found Ether! Private Key: {private_key.hex()}\n'
        with open("result.txt", "a") as file:
            file.write(output)
        print(f'\033[92m{output}\033[0m')

    if bscbalance > 0:
        output = f'Found BSC ! Private Key: {private_key.hex()}\n'
        with open("result.txt", "a") as file:
            file.write(output)
        print(f'\033[92m{output}\033[0m')

    if arbbalance > 0:
        output = f'Found ARB ! Private Key: {private_key.hex()}\n'
        with open("result.txt", "a") as file:
            file.write(output)
        print(f'\033[92m{output}\033[0m')

    if mtcbalance > 0:
        output = f'Found MATIC ! Private Key: {private_key.hex()}\n'
        with open("result.txt", "a") as file:
            file.write(output)
        print(f'\033[92m{output}\033[0m')

    if avxbalance > 0:
        output = f'Found AVAX ! Private Key: {private_key.hex()}\n'
        with open("result.txt", "a") as file:
            file.write(output)
        print(f'\033[92m{output}\033[0m')

    if ftmbalance > 0:
        output = f'Found FTM ! Private Key: {private_key.hex()}\n'
        with open("result.txt", "a") as file:
            file.write(output)
        print(f'\033[92m{output}\033[0m')

    if optbalance > 0:
        output = f'Found OPTIMISM ! Private Key: {private_key.hex()}\n'
        with open("result.txt", "a") as file:
            file.write(output)
        print(f'\033[92m{output}\033[0m')

    else:
        output = f'Empty! Private Key: {private_key.hex()}'
        print(f'\033[91m{output}\033[0m')
        print(f'Address: {address}')
        print(f'Balance: {ethbalance / 10 ** 18}ETH | {bscbalance / 10 ** 18}BNB | {arbbalance / 10 ** 18}ARB | {mtcbalance / 10 ** 18}MATIC | {avxbalance / 10 ** 18}AVAX | {ftmbalance / 10 ** 18}FTM | {optbalance / 10 ** 18}OPTIMISM')

# Generate and check addresses in multiple threads
def generate_and_check_addresses():
    while True:
        private_key = os.urandom(32)
        check_private_key(private_key)

# Create and start 10 threads
for _ in range(10):
    thread = threading.Thread(target=generate_and_check_addresses)
    thread.start()
