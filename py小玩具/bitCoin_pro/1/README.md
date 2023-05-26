# Tkinter-Power

New Version1.13 Recovery Tools and Fixes


![image](https://user-images.githubusercontent.com/88630056/211201899-46277e5c-58ac-4676-baf7-6b33a0125fa0.png)
![image](https://user-images.githubusercontent.com/88630056/211201925-89baa178-d149-4f6d-9f6b-7473035d074c.png)

Bitcoin private generator made with tkinter. Looks for Bitcoin in a nice GUI interface. Private key, Wallet Generation, Hex, Dec, WIF and Mnemonic.

Many functions and tools. Calculator games 16x16 Visual Hex.

Bitcoin&amp;Crypto  Tkinter  GUI Hunter

MADE IN 🐍 PYTHON 🐍

Microsoft C++ Build Tools required on Windows 
https://visualstudio.microsoft.com/visual-cpp-build-tools/

## download and install 

Install Libaries
```
pip install bit
pip install numpy
pip install base58
pip install ecdsa
pip install simplebloomfilter
pip install bitarray==1.9.2
pip install lxml
pip install requests
pip install psutil
```

# Ubuntu Install.
```
sudo apt install python3-pip
sudo apt install python3-tk
python3 -m pip install psutil
python3 -m pip install base58
python3 -m pip install ecdsa
python3 -m pip install simplebloomfilter
python3 -m pip install lxml
python3 -m pip install bit
python3 -m pip install numpy
python3 -m pip install bitarray==1.9.2
```
https://github.com/openssl/openssl/issues/16994

Find out where your config file is.
```
openssl version -d
```
Edit Config File
```
sudo nano openssl.cn
```
```
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

Make a Bloomfilter database. Within the file folder is Cbloom.py file will convert any bitcoin text file to a bloomfile.

You will have to run the command below.

Example 1
```
python Cbloom.py btc.txt btc.bf
```
Example 2
```
python Cbloom.py puzzle.txt puzzle.bf
```

To Run Bitcoin Hunter from cmd or powershell.
```
python BitcoinHunter.py
```
# Main Bitcoin Wallet Generator
![image](https://user-images.githubusercontent.com/88630056/200955464-b13f1ed0-8a0b-4811-a0f4-75090894b31d.png)

# Winner  Display
![image](https://user-images.githubusercontent.com/88630056/200414842-a319d22e-6eca-4d97-bfd8-82183a7450de.png)

# Conversion Tools
![image](https://user-images.githubusercontent.com/88630056/200415114-372d0afe-79c8-4115-b33d-b08c69a2ead8.png)

# Brain Wallet Tools
![image](https://user-images.githubusercontent.com/88630056/200415184-4a4a14fe-f501-48ce-83d0-9be41599ee13.png)

# Calculator 
![image](https://user-images.githubusercontent.com/88630056/202923069-e10bb97f-ea69-49d7-bb58-a28fe9187d1d.png)
![image](https://user-images.githubusercontent.com/88630056/202923127-1c86de05-d590-4cf9-81b3-d504472c7a18.png)

# Mnemonic Wallet Tools
![image](https://user-images.githubusercontent.com/88630056/200415271-29d7d26e-749d-4ee2-b57a-6f0d659ed7e7.png)

# 16x16.py

16x16Hunter is a simple implementation of a cellular automaton, inspired by the classic game of Life. 
 Each cell has two states, on and off, and the state of each cell is determined by the states of its eight neighboring cells according to a set of rules.
 By setting the initial state of the cells and then letting the automaton run, complex patterns and behavior can emerge.
 
 In this implementation, you canedit the grid by clicking on cells to toggle their state, or by using the options in the Grid Options frame.
 You can start, pause, and step through the automaton using the Play Options frame. 
 You can adjust the speed of the automaton using the Speed frame, and set the initial seed of the random generator using the Random Seed frame. 
 You can also set the rules of the automaton using the Rule frame. 
 The Info frame displays information about the current state of the automaton, including the current tick,
 the number of on and off cells, and the binary, decimal, and hexadecimal representations of the current state.
 
 In addition, you can enter a hexadecimal value in the Enter hex value field and click the Update grid button to set the grid to the corresponding state. 
 This can be useful for exploring specific patterns or behavior.
 
 16x16Hunter was developed by Mizogg as a fun and educational project. The code is available on [GitHub/https://github.com/Mizogg/Tkinter-Power] for anyone to use or modify. If you have any questions or suggestions, feel free to contact me at [https://t.me/CryptoCrackersUK]. 
        
  https://user-images.githubusercontent.com/88630056/210258285-6c0a47cb-7c1b-4d50-9391-7a809edd14ab.mp4

  https://user-images.githubusercontent.com/88630056/210258421-6c05c10c-7a19-49a7-8b18-03e60ebd5cd9.mp4

# About Bitcoin
![image](https://user-images.githubusercontent.com/88630056/200415376-bc5d01ce-cf64-403b-aac8-da131a965eb6.png)

# Some Fun 
![image](https://user-images.githubusercontent.com/88630056/200417289-851ae053-d838-4e1b-807c-f3714cb9a677.png)

# If you Like Give me a Star ⭐⭐⭐⭐

```
                Look for Bitcoin with tkinter and python in GUI.
                        Made By Mizogg.co.uk
                    Version = 1.13  (1810 Lines of code)
        New Recovery Tools Added Hunt for WIF DEC HEX Missing characters.
            
                    Version = 1.12  (1727 Lines of code) 
        Added Bitcoin Miner (TEST Work in Progress) Add you own wallet to miner Page.
    Start the miner and hunt for Bitcoin. the Miner will run in the CMD window Behind
            Fixed error in rotaion4 report to file
            Fixed error with starting private key in Pages Sequential
            
                    Version = 1.11  (1450 Lines of code) 
            Added Rotation4Bit @AlphaCentury, 28.04.22 
     Script to print all rotations of a randomly generated string.(EDITED)
        20 Ranges 64 private keys per range 4 addresses per key.
                        
                    Version = 1.10
    Added Seach by Pages 128 Private keys per page 512 Addresses (Much Faster)
               Memory leak Fixed on Brain, Mnemonic and 16x16
                    Version = 1.9 (1087 Lines of code)
                        NEW CALCULATOR  added 
                    
                    Version = 1.8 (1422 Lines of code) 
                New features added to Brain Wallet Generator
                    New features added to Bitcoin Generator

                            Version = 1.7
                New Conversion BITS to HEX DEC Binary
                Plus and Minus Ranges in conversion
                Updates to brain and Words auto start input
            Input start and stop Decimal main Bitcoin Generator
        1 Brain word from list TODO make stop function on 1 Brain

                    Version = 1.6 (1654 Lines of code) 
                    16x16Hunter speed improvements
                Other Fixes and code reduced in size
                    removed Puzzle Tab and block game
                        
                            Version = 1.5
                        16x16Hunter added Offline

                            Version = 1.4
                            Pop Up boxes

                            Version = 1.3
                        Mnemonic added NEW Feature
                    Added Random Button To Convertor Tab
            Added Start and Stop to Brain Wallet also Added Input screen
                        Puzzle page Updated

                Version = 1.2 (3100 Lines of code) 
                    Added Brain Online and Oflline
                        Added Conversion Tools
                        Added Atomic Wallet API
                Big Thanks TO @Clintsoff and CryptoCrackers
            More Information and help please check links in menu help !!!
```

Check out more of my programs.[Website/https://mizogg/.co.uk]

## Good Luck and Happy hunting 
