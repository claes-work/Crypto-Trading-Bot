import krakenex from pykrakenapi import krakenAPI
import time
import decimal
import json

k = krakenAPI(kraken_api)
df, last = kraken.get_ohlc_data('BCHUSD', ascending=True)

def now():
    return decimal.Decimal(time.time())


# get the actual balance
def get_balance():
    with open('balance.json', 'r') as file:
        try:
            return json.load(file)
        except:
            # change this for the actual query to the database once the script is working
            return {'ZUSD': '1000.0', 'EUR.HOLD': '0.0000'}


# save the actual balance
def save_balance(data):
    with open('balance.json', 'w') as file:
        json.dump(data, file, indent=4)


# update the actual balance
def update_balance(amount, name, price, sold):
    balance = get_balance()
    if sold:
        balance.pop(name[:-4], None)
        balance['ZUSD'] = str(float(balance['ZUSD'] + amount * price))
    else:
        balance['ZUSD'] = str(float(balance['ZUSD']) - (amount * price))
        balance[name[:-4]] = str(amount)
    save_balance(balance)
    return balance


# get the price data from the crypto
def get_crypto_data(pair, since):
    ret = kraken.query_public('OHLC', data={'pair': pair, 'since': since})
    return ret['result'][pair]


# load trades from the trades.json file
def load_trades():
    trades = {}
    with open('trades.json', 'r') as file:
        try:
            trades = json.load(file)
        except:
            for crypto in pairs:
                trades[crypto] = []
    return trades


# get the purchasing price in USD from the trades.json file
def get_purchasing_price(name):
    trades = load_trades()
    return trades[name][-1]['price_usd']


if __name__ == '__main__':
    k = krakenex.API()
    kraken.load_key('kraken.key')
    pairs = get_pairs()
    since = str(int(time.time() - 43200))
    mva = load_crypto_data_from_file()

    bot(since, k, pairs)