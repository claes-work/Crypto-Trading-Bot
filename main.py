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


# check a buy or sell opportunity by calculating percentage increase of each point
def check_opportunity(data, name, sell, buy):
    count = 0
    previous_value = 0
    trends = []
    for mva in data['close'][-10:]:
        if previous_value == 0:
            previous_value = mva
        else:
            if mva / previous_value > 1:
                # uptrend
                if count < 1:
                    count = 1
                else:
                    count += 1
                trends.append('UPTREND')
            elif mva / previous_value < 1:
                trends.append('DOWNTREND')
                if count > 0:
                    count = -1
                else:
                    count -= 1
            else:
                trends.append('NOTREND')
            previous_value = mva
        areas = []
        for mva in reversed(data['close'][-5:]):
            area = 0
            price = float(data['prices'][-1][3])
            if sell:
                purchase_price = float(get_purchasing_price(name))
                if price >= (purchase_price * 1.02):
                    print('Should sell with 10% profit')
                    return True
                if price < purchase_price:
                    print('Selling at a loss')
                    return True
            areas.append(mva / price)

        if buy:
            counter = 0
            if count >= 5:
                for area in areas:
                    counter += area
                if counter / 3 >= 1.05:
                    return True
        return False


# analyse the data to see if it is a good opportunity to buy and try to buy if so
def try_buy(data, name, crypto_data):
    make_trade = check_opportunity(data, name, False, True)
    if make_trade:
        buy_crypto(crypto_data, name)


# analyse the data to see if it is a good opportunity to sell and try to sell if so
def try_sell(data, name, crypto_data):
    make_trade = check_opportunity(data, name, True, False)
    if make_trade:
        sell_crypto(crypto_data, name)


# check the crypto data and try to buy or sell
def check_data(name, crypto_data, should_buy):
    high = 0
    low = 0
    close = 0
    for b in crypto_data[-100:]:
        if b not in mva[name]['prices']:
            mva[name]['prices'].append(b)
        high += float(b[2])
        low += float(b[3])
        close += float(b[4])
    mva[name]['high'].append(high / 100)
    mva[name]['low'].append(low / 100)
    mva[name]['close'].append(close / 100)
    save_crypto_data(mva)
    if should_buy:
        try_buy(mva[name], name, crypto_data)
    else:
        try_sell(mva[name], name, crypto_data)


# the bot that is buying and selling after checking each crypto pairs every 20 seconds
def bot(since, k, pairs):
    while True:
        # comment out to track the same 'since'
        # since = ret['result']['last']
        for pair in pairs:
            trades = load_trades()
            if len(trades[pair]) > 0:
                crypto_data = get_crypto_data(pair, since)
                if trades[pair][-1]['sold'] or trades[pair][-1] is None:
                    # check if the bot should buy
                    check_data(pair, crypto_data, True)
                if trades[pair][-1]['bought']:
                    # check if the bot should sell
                    check_data(pair, crypto_data, False)
            else:
                crypto_data = get_crypto_data(pair, since)
                check_data(pair, crypto_data, True)

        time.sleep(20)


# control structure system variable __main__
if __name__ == '__main__':
    k = krakenex.API()
    kraken.load_key('kraken.key')
    pairs = get_pairs()
    since = str(int(time.time() - 43200))
    mva = load_crypto_data_from_file()

    bot(since, k, pairs)