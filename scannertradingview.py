import requests
import json
from object_types.tradingviewmodel import *


class ScannerTradingview:
    def __init__(self):
        self.requestJson = '''{
            "filter": [
                {
                    "left": "type",
                    "operation": "in_range",
                    "right": [
                        "stock",
                        "dr",
                        "fund"
                    ]
                },
                {
                    "left": "subtype",
                    "operation": "in_range",
                    "right": [
                        "common",
                        "foreign-issuer",
                        "",
                        "etf",
                        "etf,odd",
                        "etf,otc",
                        "etf,cfd"
                    ]
                },
                {
                    "left": "volume",
                    "operation": "egreater",
                    "right": 1000000
                },
                {
                    "left": "change",
                    "operation": "greater",
                    "right": 1
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
                    "left": "is_primary",
                    "operation": "equal",
                    "right": true
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
                    "right": "close"
                },
                {
                    "left": "VWMA",
                    "operation": "less",
                    "right": "high"
                }
            ],
            "options": {
                "lang": "en"
            },
            "markets": [
                "indonesia"
            ],
            "symbols": {
                "query": {
                    "types": []
                },
                "tickers": []
            },
            "columns": [
                "name"
            ],
            "sort": {
                "sortBy": "price_earnings_ttm",
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
        self.url = 'https://scanner.tradingview.com/indonesia/scan'

    def getDataScanner(self):
        result = requests.post(self.url, data=self.requestJson)
        data = json.loads(result.text)
        return [i['d'][0] for i in data["data"]]
