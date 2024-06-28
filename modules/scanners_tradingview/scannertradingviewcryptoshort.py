import requests
import json
from object_types.tradingviewmodel import *


class ScannerTradingviewCryptoShort:
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
                    "operation": "less",
                    "right": 0
                },
                {
                    "left": "change_from_open_abs",
                    "operation": "less",
                    "right": 0
                },
                {
                    "left": "RSI",
                    "operation": "eless",
                    "right": 70
                },
                {
                    "left": "RSI7",
                    "operation": "eless",
                    "right": 70
                },
                {
                    "left": "EMA5",
                    "operation": "greater",
                    "right": "close"
                },
                {
                    "left": "EMA10",
                    "operation": "greater",
                    "right": "close"
                },
                {
                    "left": "Stoch.K",
                    "operation": "eless",
                    "right": 80
                },
                {
                    "left": "Stoch.D",
                    "operation": "eless",
                    "right": 80
                },
                {
                    "left": "CCI20",
                    "operation": "eless",
                    "right": 100
                },
                {
                    "left": "HullMA9",
                    "operation": "greater",
                    "right": "close"
                },
                {
                    "left": "Stoch.RSI.K",
                    "operation": "eless",
                    "right": 80
                },
                {
                    "left": "Stoch.RSI.D",
                    "operation": "eless",
                    "right": 80
                },
                {
                    "left": "W.R",
                    "operation": "less",
                    "right": -20
                },
                {
                    "left": "VWAP",
                    "operation": "greater",
                    "right": "close"
                },
                {
                    "left": "VWMA",
                    "operation": "greater",
                    "right": "low"
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
                "sortBy": "change",
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
