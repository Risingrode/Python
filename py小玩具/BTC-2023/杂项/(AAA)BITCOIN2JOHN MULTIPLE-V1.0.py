import binascii
import logging
import struct
import sys
import tkinter as tk

from bsddb.dbobj import DB


def hexstr(bytestr):
    return binascii.hexlify(bytestr).decode('ascii')

from tkinter import filedialog

try:
    from bsddb.db import *
except:
    try:
        from bsddb.db import *
    except:
        sys.stderr.write("Error: This script needs bsddb3 to be installed!\n")
        sys.exit(1)

# bitcointools wallet.dat handling code
class SerializationError(Exception):
    """ Thrown when there's a problem deserializing or serializing """

class BCDataStream(object):
    def __init__(self):
        self.input = None
        self.read_cursor = 0

    def clear(self):
        self.input = None
        self.read_cursor = 0

    def write(self, bytes):  # Initialize with string of bytes
        if self.input is None:
            self.input = bytes
        else:
            self.input += bytes

    def read_string(self):
        # Strings are encoded depending on length:
        # 0 to 252 :    1-byte-length followed by bytes (if any)
        # 253 to 65,535 : byte'253' 2-byte-length followed by bytes
        # 65,536 to 4,294,967,295 : byte '254' 4-byte-length followed by bytes
        # ... and the Bitcoin client is coded to understand:
        # greater than 4,294,967,295 : byte '255' 8-byte-length followed by bytes of string
        # ... but I don't think it actually handles any strings that big.
        if self.input is None:
            raise SerializationError("call write(bytes) before trying to deserialize")

        try:
            length = self.read_compact_size()
        except IndexError:
            raise SerializationError("attempt to read past end of buffer")

        return self.read_bytes(length).decode('ascii')

    def read_bytes(self, length):
        try:
            result = self.input[self.read_cursor:self.read_cursor + length]
            self.read_cursor += length
            return result
        except IndexError:
            raise SerializationError("attempt to read past end of buffer")

        return ''

    def read_uint32(self):
        return self._read_num('<I')

    def read_compact_size(self):
        size = self.input[self.read_cursor]
        if isinstance(size, str):
            size = ord(self.input[self.read_cursor])
        self.read_cursor += 1
        if size == 253:
            size = self._read_num('<H')
        elif size == 254:
            size = self._read_num('<I')
        elif size == 255:
            size = self._read_num('<Q')
        return size

    def _read_num(self, format):
        (i,) = struct.unpack_from(format, self.input, self.read_cursor)
        self.read_cursor += struct.calcsize(format)
        return i

def open_wallet(walletfile):
    db = DB()
    DB_TYPEOPEN = DB_RDONLY
    flags = DB_THREAD | DB_TYPEOPEN
    try:
        r = db.open(walletfile, "main", DB_BTREE, flags)
    except DBError as e:
        logging.error(e)
        r = True

    if r is not None:
        logging.error("Couldn't open wallet.dat/main. Try quitting Bitcoin and running this again.")
        logging.error("See our doc/README.bitcoin for how to setup and use this script correctly.")
        sys.exit(1)

    return db

def parse_wallet(db, item_callback):
    kds = BCDataStream()
    vds = BCDataStream()

    for (key, value) in db.items():
        d = { }

        kds.clear()
        kds.write(key)
        vds.clear()
        vds.write(value)

        type = kds.read_string()

        d["__key__"] = key
        d["__value__"] = value
        d["__type__"] = type

        try:
            if type == "mkey":
                d['encrypted_key'] = vds.read_bytes(vds.read_compact_size())
                d['salt'] = vds.read_bytes(vds.read_compact_size())
                d['nDerivationMethod'] = vds.read_uint32()
                d['nDerivationIterations'] = vds.read_uint32()

            item_callback(type, d)

        except Exception:
            sys.stderr.write("ERROR parsing wallet.dat, type %s\n" % type)
            sys.stderr.write("key data in hex: %s\n" % hexstr(key))
            sys.stderr.write("value data in hex: %s\n" % hexstr(value))
            sys.exit(1)

def read_wallet(json_db, walletfile):
    db = open_wallet(walletfile)

    json_db['mkey'] = {}

    def item_callback(type, d):
        if type == "mkey":
            json_db['mkey']['encrypted_key'] = hexstr(d['encrypted_key'])
            json_db['mkey']['salt'] = hexstr(d['salt'])
            json_db['mkey']['nDerivationMethod'] = d['nDerivationMethod']
            json_db['mkey']['nDerivationIterations'] = d['nDerivationIterations']

    parse_wallet(db, item_callback)

    db.close()

    crypted = 'salt' in json_db['mkey']

    if not crypted:
        sys.stderr.write("%s: this wallet is not encrypted\n" % walletfile)
        return -1

    return {'crypted': crypted}

# GUI class for file selection
class WalletCrackerGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Wallet Cracker")
        self.geometry("400x200")

        self.file_paths = []

        self.label = tk.Label(self, text="Select wallet.dat files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self, text="Select files", command=self.select_files)
        self.select_button.pack()

        self.crack_button = tk.Button(self, text="Crack wallets", command=self.crack_wallets)
        self.crack_button.pack(pady=10)

    def select_files(self):
        self.file_paths = filedialog.askopenfilenames(filetypes=[("Wallet files", "*.dat")])

        
    def crack_wallets(self):
        if len(self.file_paths) == 0:
            sys.stderr.write("No wallet files selected!\n")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not output_file:
            sys.stderr.write("No output file selected!\n")
            return

        with open(output_file, "w") as f:
            for file_path in self.file_paths:
                json_db = {}
                result = read_wallet(json_db, file_path)

                if result == -1:
                    continue

                cry_master = binascii.unhexlify(json_db['mkey']['encrypted_key'])
                cry_salt = binascii.unhexlify(json_db['mkey']['salt'])
                cry_rounds = json_db['mkey']['nDerivationIterations']
                cry_method = json_db['mkey']['nDerivationMethod']

                crypted = 'salt' in json_db['mkey']

                if not crypted:
                    sys.stderr.write("%s: this wallet is not encrypted\n" % file_path)
                    continue

                if cry_method != 0:
                    sys.stderr.write("%s: this wallet uses an unknown key derivation method\n" % file_path)
                    continue

                cry_salt = json_db['mkey']['salt']

                if len(cry_salt) == 16:
                    expected_mkey_len = 96  # 32 bytes padded to 3 AES blocks (last block is padding-only)
                elif len(cry_salt) == 36:  # Nexus legacy wallet
                    expected_mkey_len = 160  # 72 bytes padded to whole AES blocks
                else:
                    sys.stderr.write("%s: this wallet uses an unsupported salt size\n" % file_path)
                    continue

                if len(json_db['mkey']['encrypted_key']) != expected_mkey_len:
                    sys.stderr.write("%s: this wallet uses an unsupported master key size\n" % file_path)
                    continue

                cry_master = json_db['mkey']['encrypted_key'][-64:]  # last two AES blocks are enough

                f.write("$bitcoin$%s$%s$%s$%s$%s$2$00$2$00\n" % (len(cry_master), cry_master, len(cry_salt), cry_salt, cry_rounds))

        sys.stdout.write("Wallets cracked successfully!\n")

if __name__ == '__main__':
    app = WalletCrackerGUI()
    app.mainloop()

