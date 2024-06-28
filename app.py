import json
import requests
from flask import Flask, request
from modules.imapprocessing import *
from modules.scanners_tradingview.scannertradingviewstock import ScannerTradingviewStock
from modules.scanners_tradingview.scannertradingviewcryptolong import ScannerTradingviewCryptoLong
from modules.scanners_tradingview.scannertradingviewcryptoshort import ScannerTradingviewCryptoShort

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Welcome to My Website</h1>"


@app.route('/crypto_long_screening', methods=['POST'])
def crypto_long_screening():
    process = ImapProcessing()
    process.long_crypto_signal()
    return "<h1>Crypto LONG Screening Has Send to Telegram</h1>"


@app.route('/crypto_short_screening', methods=['POST'])
def crypto_short_screening():
    process = ImapProcessing()
    process.short_crypto_signal()
    return "<h1>Crypto SHORT Screening Has Send to Telegram</h1>"


@app.route('/crypto_long_screening_debug', methods=['POST'])
def crypto_long_screening_debug():
    scanner = ScannerTradingviewCryptoLong()
    data = scanner.getDataScanner()
    process = ImapProcessing()
    process.long_crypto_signal_debug(data)
    return "<h1>Stock Screening Has Send to Telegram</h1>"


@app.route('/crypto_short_screening_debug', methods=['POST'])
def crypto_short_screening_debug():
    scanner = ScannerTradingviewCryptoShort()
    data = scanner.getDataScanner()
    process = ImapProcessing()
    process.short_crypto_signal_debug(data)
    return "<h1>Stock Screening Has Send to Telegram</h1>"


@app.route('/stock_screening', methods=['POST'])
def stock_screening():
    process = ImapProcessing()
    process.stock_signal()
    return "<h1>Stock Screening Has Send to Telegram</h1>"


@app.route('/stock_screening_debug', methods=['POST'])
def stock_screening_debug():
    scanner = ScannerTradingviewStock()
    data = scanner.getDataScanner()
    process = ImapProcessing()
    process.stock_signal_debug(data)
    return "<h1>Stock Screening Has Send to Telegram</h1>"


def send_to_telegram(messages):
    URL = "https://api.telegram.org/bot5081508998:AAGf-rPpts71oaXRu4eBRZZYVVHJWgsBojQ/sendMessage"
    message = messages
    PARAMS = {'chat_id': '-640350956', 'text': message}
    requests.get(url=URL, params=PARAMS)


@app.route('/bnbsdtperp_momentum_up', methods=['POST'])
def bnbusdtperp_momentum_up():
    data = json.loads(request.data)
    open = data['open']
    close = data['close']
    if (open > close):
        send_to_telegram("[BNBUSDTPERP] MOMENTUM DOWN ")
    else:
        send_to_telegram("[BNBUSDTPERP] MOMENTUM UP ")
    return "<h1>BNBUSDTPERP Momentum Up</h1>"
