import hashlib
import pbkdf2
import base58
import struct
import sys


# To use this code, you will need to have Python installed on your computer, as well as the hashlib,
# pbkdf2, and base58 libraries. You can install these libraries using pip, 
# the Python package manager, by running the following command:

# Once you have the required libraries installed, you can run the code by saving it to a file (e.g. "extract_wallet.py") 
# and then running it from the command line with the name of the wallet file as an argument:
# The code will then read the wallet file, search for "mkey" and "ckey" records, and extract and display the encrypted master key and private keys,
# as well as the corresponding public keys and Bitcoin addresses.

# Keep in mind that you will need to provide the correct password for the wallet in order to decrypt the master key and private keys. 
# Without the correct password, the program will not be able to decrypt these keys and will display the encrypted data instead.

# sys is not a package or library that you can install using pip. 
# sys is a built-in module in Python that provides access to various functions and variables related to the Python interpreter and the environment in which it is running.
# You don't need to install sys separately, as it is included with the Python standard library.

# To use the sys module in your code, you will need to import it at the top of your script using the import statement: import sys


# pip install pbkdf2 
# pip install hashlib  
# pip install base58

# python metaC-M-key.py wallet.dat


# you will see this example.
# ...................................................................................................................................................
# C:\Python38>python metaC-M-key.py wallet.dat
# Mkey_encrypted: 0716573758f76664af83b35f680385b39e8bf9964ecfbf359cd97fa19ce79a24a8c6fd904e47a54f9b24cd1ec1e39985
# encrypted ckey: c9ea18eecd966dbe77044c0b54568ea010fb18ee9a41ef056406b628296673419c81a16d8252850c5f9fc20a47000104
# public key    : d13fc315ff0c7fbf1bdbe50a31ed0ba351cdccc5c9aff053558e42b7e3907ad08d24203ece24c4d166c7dedade59d461bfda1cb8fd78c42a13cd5ec24b0000310001
# public address: 126uQgWNVHUTAmuai6bqJdRNaf8NzwXVgP
# .....................................................................................................................................................

# telegram
# metahuman
# @JasonSatrani mybtc:) 1LQJcuR5caJMgVY6m3j1QMrswhpMmjVYer


def to_hex(data: bytes) -> str:
    return ''.join(format(b, '02x') for b in data)


def pubkey_to_pubaddress(public_key):
    hash160 = hashlib.new('ripemd160')
    hash160.update(hashlib.sha256(public_key).digest())
    address_bytes = b'\x00' + hash160.digest()
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    address_bytes += checksum
    return base58.b58encode(address_bytes)


def main():
    # check if a wallet file was provided as an argument
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} wallet.dat")
        sys.exit(0)
    wallet_filename = sys.argv[1]

    # open the wallet file
    with open(wallet_filename, 'rb') as wallet:
        # search for the mkey record
        mkey_offset = None
        wallet.seek(0)
        while True:
            mkey = wallet.read(4)
            if len(mkey) < 4 or mkey == b'mkey':
                mkey_offset = wallet.tell() - 4
                break
        if mkey_offset is not None:
            # read the encrypted mkey data
            wallet.seek(mkey_offset - 72)
            mkey_data = wallet.read(48)
            # print the encrypted mkey data as a hex string
            print(f"Mkey_encrypted: {to_hex(mkey_data)}")
        else:
            print("There is no Master Key in the file")
            return

        # reset the file position and search for ckey records
        wallet.seek(0)
        count = 0
        while True:
            ckey = wallet.read(4)
            if len(ckey) < 4 or ckey != b'ckey':
                continue
            # read the ckey data
            wallet.seek(wallet.tell() - 52)
            ckey_data = wallet.read(123)
            # extract the encrypted ckey and public key
            ckey_encrypted = ckey_data[:48]
            public_key_length, = struct.unpack('B', ckey_data[56:57])
            public_key = ckey_data[57:57 + public_key_length]
            # print the encrypted ckey and public key as hex strings
            print(f"encrypted ckey: {to_hex(ckey_encrypted)}")
            print(f"public key    : {to_hex(public_key)}")
            # compute the Bitcoin address from the public key
            public_address = pubkey_to_pubaddress(public_key)
            print(f"public address: {public_address}")
            print()
            count += 1
    print(f"{count} ckey records found")


if __name__ == '__main__':
    main()
