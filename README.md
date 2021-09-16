# Crypto-Trading-Bot
An easy to use python script to ride up- and downtrends on an intraday basis using the kraken API.

## :warning: **WARNING!**
**I do not recommend using this bot! Doing so is at your on risk. I am not responsible for any losses that come along with it. Keep in mind that cryptocurrencies have a hight volatility and that most of all private investors are loosing money by trading them on an intra day basis.**

Note that although the script worked in a short periode of testing, this could be still due some disregarded parameters.
I am not an expert in cryptocurrency trading and there are plenty of reasons why an usage of this script could fail.

Since I don't want you to loose money, there is **no detailed installation guide**.
However if you have an basic understanding of [![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white&link=https://www.python.org/)](https://www.python.org/) and you're actually understanding how the code works, feel free to use or extend it.

## ⚙️ How it works 
The script works on the basis of a market chart price pattern, that detects higher highs and higher lows. This is an extremly popular approach to define an up- or downtrend.
If the price continue rising above the last high means that we have a new higher high, which is indecating an uptrend. If on the other hand the price sinks below the last low means that we have a new lower low, which is indecating an downtrend. 

![higher high lower low](https://github.com/claes-work/claes-work/blob/main/Images/higher_high_lower_low.png?raw=true)
