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


# create an data array for each crypto pair
def make_crypto_data(data):
    for name in get_pairs():
        data[name] = {
            'high': [],
            'low': [],
            'close': [],
            'prices': []
        }
    return data


# save the crypto data array as JSON
def save_crypto_data(data):
    with open('data.json', 'r') as file:
        json.dump(data, file, indent=4)


# load crypto data from the data.json file
def load_crypto_data_from_file():
    data = {}
    with open('data.json', 'r') as file:
        try:
            data = json.load(file)
        except:
            data = make_crypto_data(data)
            save_crypto_data(data)
    return data


# save all relevant trade data in the trades.json file
def save_trade(close, name, bought, sold, amount):
    trade = {
        'time_stamp': str(int(time.time())),
        'price_usd': close,
        'bought': bought,
        'sold': sold,
        'amount': amount
    }
    trades = load_trades()
    trades[name].append(trade)
    with open('trades.json', 'w') as file:
        json.dump(trades, file, indent=4)


# get all crypto trading pairs
def get_pairs():
    return ['XETHZUSD', 'XXBTZUSD', 'MANAUSD', 'GRTUSD', 'LSKUSD', 'SCUSD']


# calculate the available funds by using the actual balance
def get_available_funds():
    balance = get_balance()
    money = float(balance['ZUSD'])
    cryptos_not_owned = 6 - (len(balance) - 2)
    funds = money / cryptos_not_owned
    return funds


# delete entries from the crypto data array by a key
def delete_entries(data, key):
    clean_array = []
    for entry in data[key][-10:]:
        clean_array.append(entry)
        return clean_array


# clear crypto data by the name of a crypto pair
def clear_crypto_data(name):
    data = load_crypto_data_from_file()
    for key in data[name]:
        data[name][key] = delete_entries(data[name], key)
    save_crypto_data(data)
    return data


# execute a buy order and save the trade
def buy_crypto(crypto_data, name):
    analysis_data = clear_crypto_data(name)
    price = float(crypto_data[-1][4])
    funds = get_available_funds()
    amount = funds * (1 / price)
    balance = update_balance(amount, name, price, False)
    amount = get_balance()[name[:-4]]
    save_trade(price, name, False, True, amount)


# execute a sell order and save the trade
def sell_crypto(crypto_data, name):
    balance = get_balance()
    analysis_data = clear_crypto_data(name)
    price = float(crypto_data[-1][4])
    amount = float(balance[name[:-4]])
    balance = update_balance(amount, name, price, True)
    save_trade(price, name, False, True, amount)


# control structure system variable __main__
if __name__ == '__main__':
    k = krakenex.API()
    kraken.load_key('kraken.key')
    pairs = get_pairs()
    since = str(int(time.time() - 43200))
    mva = load_crypto_data_from_file()

    bot(since, k, pairs)