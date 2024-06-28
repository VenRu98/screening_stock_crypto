import requests
import json
from object_types.tradingviewmodel import *


class ScannerTradingviewCryptoLong:
    def __init__(self):
        self.requestJson = '''{
            "filter": [
                {
                    "left": "exchange",
                    "operation": "equal",
                    "right": "BINANCE"
                },
                {
                    "left": "volume",
                    "operation": "in_range",
                    "right": [
                        1000,
                        9007199254740991
                    ]
                },
                {
                    "left": "change_from_open",
                    "operation": "greater",
                    "right": 0
                },
                {
                    "left": "change_from_open_abs",
                    "operation": "greater",
                    "right": 0
                },
                {
                    "left": "RSI",
                    "operation": "egreater",
                    "right": 30
                },
                {
                    "left": "RSI7",
                    "operation": "egreater",
                    "right": 30
                },
                {
                    "left": "EMA5",
                    "operation": "less",
                    "right": "close"
                },
                {
                    "left": "EMA10",
                    "operation": "less",
                    "right": "close"
                },
                {
                    "left": "Stoch.K",
                    "operation": "egreater",
                    "right": 20
                },
                {
                    "left": "Stoch.D",
                    "operation": "egreater",
                    "right": 20
                },
                {
                    "left": "CCI20",
                    "operation": "egreater",
                    "right": -100
                },
                {
                    "left": "HullMA9",
                    "operation": "less",
                    "right": "close"
                },
                {
                    "left": "Stoch.RSI.K",
                    "operation": "egreater",
                    "right": 20
                },
                {
                    "left": "Stoch.RSI.D",
                    "operation": "egreater",
                    "right": 20
                },
                {
                    "left": "W.R",
                    "operation": "greater",
                    "right": -80
                },
                {
                    "left": "VWAP",
                    "operation": "less",
                    "right": "high"
                },
                {
                    "left": "VWMA",
                    "operation": "less",
                    "right": "close"
                }
            ],
            "options": {
                "lang": "en"
            },
            "markets": [
                "crypto"
            ],
            "symbols": {
                "query": {
                    "types": []
                },
                "tickers": []
            },
            "columns": [
                "base_currency_logoid",
                "currency_logoid",
                "name",
                "close",
                "change",
                "change_abs",
                "high",
                "low",
                "volume",
                "24h_vol|5",
                "24h_vol_change|5",
                "Recommend.All",
                "exchange",
                "description",
                "type",
                "subtype",
                "update_mode",
                "pricescale",
                "minmov",
                "fractional",
                "minmove2"
            ],
            "sort": {
                "sortBy": "name",
                "sortOrder": "desc"
            },
            "price_conversion": {
                "to_symbol": false
            },
            "range": [
                0,
                150
            ]
        }'''
        self.url = 'https://scanner.tradingview.com/crypto/scan'

    def getDataScanner(self):
        result = requests.post(self.url, data=self.requestJson)
        data = json.loads(result.text)
        return [i['d'][0] for i in data["data"]]
