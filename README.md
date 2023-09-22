# Proxyus version 4.0
## Description
Program for finding and checking proxies. Finds both from certain sources and by searching for their open sources. Checks proxy performance, IP geolocation and protocol.
Tested on Ubuntu 22.04, Kali 2023.2, python 3.10+.

## Features
* The search is carried out asynchronously, finds up to 4000 proxies in 5 seconds.
* Checked multi-threaded, 4000 proxies in one minute.
* It is possible to save the results to a file.
* You can use Tor when searching.
___
### Installation method and run
    git clone https://github.com/vomanc/Proxyus.git
    cd Proxyus
    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt
    python3 proxyus.py -h
___
### Recommended
Add API keys in extension.py>IPINFO_TOKEN
* IPINFO_TOKEN: https://ipinfo.io/
___
### Examples running:
	python3 proxyus.py
	python3 proxyus.py -c
	python3 proxyus.py -d 1 -c
___
## Author: @vomanc
___
### Tech Stack

* __python3__
___
### Donation
![Bitcoin](https://www.blockchain.com/explorer/_next/static/media/bitcoin.df7c9480.svg) BTC
* bc1q8ymcf78f4qwjlyj9v7q3ujtqm8nm9e3rms3rcq

![Ethereum](https://www.blockchain.com/explorer/_next/static/media/ethereum.57ab686e.svg) ETH
* 0x015a50222160E7EF9d0ED030BA232025234D0f82

![Tether](https://www.blockchain.com/explorer/_next/static/media/usdt.dd7e4bef.svg) USDT
* 0x015a50222160E7EF9d0ED030BA232025234D0f82
---
![WebMoney](https://www.webmoney.ru/favicon-32x32.png)
### WebMoney
* WMZ: Z826298065674
* WME: E786709266824
