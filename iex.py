import os
import requests
import json
from api_fetch import getIEX_API_KEY
from api_fetch import getIEX_API_KEY_TEST

API_KEY = getIEX_API_KEY()
API_KEY_TEST = getIEX_API_KEY_TEST()

def getQuote(symbol):
    print("Fetching " + symbol +  " quote")
    #base_url is using sandbox for testing purposes
    base_url = "https://sandbox.iexapis.com/stable/stock/{}/quote?token={}"
    request_url = base_url.format(symbol,API_KEY_TEST) 
    r = requests.get(request_url)
    data = r.text
    data_dict = json.loads(data)
    quote = data_dict['latestPrice']
    return quote

def getSeries(symbol, time):
    print("Fetching " + symbol +  " series")
    #base_url is using sandbox for testing purposes
    base_url = "https://sandbox.iexapis.com/stable/stock/{}/chart/{}?token={}"
    request_url = base_url.format(symbol, time, API_KEY_TEST)
    r = requests.get(request_url)
    data = r.text
    data_dict = json.loads(data)
    closing_prices = []
    for key in data_dict:
        closing_prices.append(key['close'])
    return closing_prices

def main():
    #getQuote("BA")
    getSeries("BA", "1y")

if __name__ == "__main__":
    main()