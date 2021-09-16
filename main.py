import krakenex from pykrakenapi import krakenAPI
import time
import decimal
import json

k = krakenAPI(kraken_api)
df, last = kraken.get_ohlc_data('BCHUSD', ascending=True)