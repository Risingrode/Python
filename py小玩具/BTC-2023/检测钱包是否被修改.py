import os
from tkinter.filedialog import askopenfilenames,askdirectory
# Prompt the user for the path to the wallet.dat file

# wallet_dat_file_path = askopenfilenames()
wallet_dat_file_path = askdirectory()
# Check if the wallet.dat file exists
if not os.path.exists(wallet_dat_file_path):
    print("Wallet.dat file does not exist. It may be fake.")
else:
    # Check file size
    file_size = os.path.getsize(wallet_dat_file_path)
    if file_size == 0:
        print("Wallet.dat file is empty. It may be fake.")
    else:
        # Read the contents of the file
        with open(wallet_dat_file_path, 'rb') as f:
            file_data = f.read()

            # Perform custom analysis based on specific characteristics or properties
            if b'bitcoin' in file_data and b'\x00\x00\x00\x00' in file_data:
                # Example: Check if the string 'bitcoin' and null bytes are present in the file
                print("Wallet.dat file appears to be real.")
            else:
                print("Wallet.dat file does not match expected characteristics. It may be fake.")