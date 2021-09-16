import krakenex from pykrakenapi import krakenAPI
import time
import decimal
import json

k = krakenAPI(kraken_api)
df, last = kraken.get_ohlc_data('BCHUSD', ascending=True)

def now():
    return decimal.Decimal(time.time())


def get_balance():
    with open('balance.json', 'r') as file:
        try:
            return json.load(file)
        except:
            # change this for the actual query to the database once the script is working
            return {'ZUSD': '1000.0', 'EUR.HOLD': '0.0000'}


def save_balance(data):
    with open('balance.json', 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    k = krakenex.API()
    kraken.load_key('kraken.key')
    pairs = get_pairs()
    since = str(int(time.time() - 43200))
    mva = load_crypto_data_from_file()

    bot(since, k, pairs)