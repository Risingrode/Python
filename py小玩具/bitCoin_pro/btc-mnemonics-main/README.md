#  Bitcoin Brute Mnemonics
Try to find/match Mnemonics Key from Bitcoin address list.

```
sudo apt-get install libssl-dev build-essential automake pkg-config libtool libffi-dev libgmp-dev
```
```
pip3 install -r requirements.txt
```
```
python3 btc-mnemonics.py
```
<br>change line '148' :
<br>entropy_bits = 128 # for 12 Mnemonics word
<br>entropy_bits = 256 # for 24 Mnemonics word

<p>Download letest bitcon address with balance
<br>here : http://addresses.loyce.club/
<br>change line 19 "fl = 'btc-rich.txt'" for bitcoin address list.

<p>if have problem with "ValueError: unsupported hash type ripemd160" (just for python3)
<br>check here : https://stackoverflow.com/questions/72409563/unsupported-hash-type-ripemd160-with-hashlib-in-python

<p>
<img src="https://github.com/rouze-d/btc-mnemonics/blob/main/screenshot.png"/>
<br>
<h2> IMPOSSIBLE !! but maybe you're God favorite person.
