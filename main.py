import krakenex from pykrakenapi import krakenAPI
import time
import decimal
import json

k = krakenAPI(kraken_api)
df, last = kraken.get_ohlc_data('BCHUSD', ascending=True)



if __name__ == '__main__':
    k = krakenex.API()
    kraken.load_key('kraken.key')
    pairs = get_pairs()
    since = str(int(time.time() - 43200))
    mva = load_crypto_data_from_file()

    bot(since, k, pairs)