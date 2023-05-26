# jay-bit-hash
## Overview
jay-bit-hash is a terminal based, Python application attempting to crack future results in an online casino game called Bustabit (currently version 2 of Bustabit). The terminal application uses the Rich Python library for neatly formatted output in the terminal, such that the user can get relevant information about the hash cracking process. Keep in mind, this is a multithreaded application and will consume a significant portion of your computers resources. This application is not meant to be used while you're doing anything CPU intensive.  

Please keep in mind that running this application in no way is a guarantee of winning. In fact, the chance of finding a winning hash is equal to: 2^256 / the number of games left in bustabit (< 10 million). I would like to think of it as more of a proof of concept with the possibility of winning the jackpot. This is your warning not to fry your computer running this application.  

![Terminal](https://github.com/Jay-ArBrouillard/jay-bit-hash/blob/master/terminal.PNG?raw=true)

## Terminology
Latest Terminating Hash - is the latest SHA256 hash pulled from Bustabit.com. This application will periodically update this value.  
Maximum Hashes Executed Per Thread - is the amount of hashes to look into the future. This is set to 2880 hashes which is estimated to be about 1 days worth of hashes ahead. The higher this value is set to the less hashes per minute will be tested per hour. You can change this value by searching for "MAX_ITERATIONS" in main.py but I would go much lower than this unless you are watching the program run yourself.
Winning Hash - if this value is not N/A, then you won. You can use this hash to find the result of all games that came before it. See the open-source [verification tool](https://jsfiddle.net/Dexon95/2fmuxLza/show).  
Threads (Section) - shows the randomly generated hash each thread is currently checking. There will be a line per thread available on your CPU. Thus, more threads and/or more powerful CPU cores will result in more hashes per hour checked.  

## Compatibility
Works with Linux, OSX, and Windows. Requires Python 3.6.3 or later.

## Requirements
Install the required Python packages. I'd suggest creating an virtual environment, activating the environment, and then installing dependencies there instead of installing the dependencies globally.

```sh
# Optionally create and activate virtual environment
virtualenv venv
source venv/bin/activate ## This is the linux syntax. For windows it look something like: venv\Scripts\activate

pip install -r requirements.txt
```

## Run it
Run the main python file.
```sh
py main.py
```

## Donations
If you win the jackpot with this code, feel free to donate as a token of appreciation :)  
BTC: `17mXG71RKDGN14YFtAb1mM2cUPctvvuFsp`
