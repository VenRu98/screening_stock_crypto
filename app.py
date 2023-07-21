import json
import requests
from flask import Flask, request
from modules.imapprocessing import *

app= Flask(__name__)

  # {"data" : [
  #     "BAPA"
  #     ,"BIRD"
  #     ,...
  # ]}

#   var dataset = "";
# for (let index = 0; index < 32; index++) {
#     var data = $(`#bottom-area > div.bottom-widgetbar-content.screener.tv-screener > div.tv-screener__content-pane.tv-screener__content-pane--fully-loaded > table > tbody > tr:nth-child(${index+1}) > td.tv-data-table__cell.apply-common-tooltip.tv-screener-table__cell.tv-screener-table__cell--left.tv-screener-table__cell--with-marker > div > div.tv-screener-table__symbol-container-description > div`).text();    
#     dataset+=`"${data}",`;
# }

@app.route('/')
def index():
  return "<h1>Welcome to My Website</h1>"

@app.route('/crypto_long_screening',methods=['POST'])
def crypto_long_screening():
    process = ImapProcessing()
    process.long_crypto_signal()
    return"<h1>Crypto LONG Screening Has Send to Telegram</h1>"

@app.route('/crypto_short_screening',methods=['POST'])
def crypto_short_screening():
    process = ImapProcessing()
    process.short_crypto_signal()
    return"<h1>Crypto SHORT Screening Has Send to Telegram</h1>"

@app.route('/crypto_long_screening_debug',methods=['POST'])
def crypto_long_screening_debug():
  data = json.loads(request.data)['data']
  process = ImapProcessing()
  process.long_crypto_signal_debug(data)
  return"<h1>Stock Screening Has Send to Telegram</h1>"

@app.route('/crypto_short_screening_debug',methods=['POST'])
def crypto_short_screening_debug():
  data = json.loads(request.data)['data']
  process = ImapProcessing()
  process.short_crypto_signal_debug(data)
  return"<h1>Stock Screening Has Send to Telegram</h1>"

@app.route('/stock_screening',methods=['POST'])
def stock_screening():
    process = ImapProcessing()
    process.stock_signal()
    return"<h1>Stock Screening Has Send to Telegram</h1>"

@app.route('/stock_screening_debug',methods=['POST'])
def stock_screening_debug():
  data = json.loads(request.data)['data']
  process = ImapProcessing()
  process.stock_signal_debug(data)
  return"<h1>Stock Screening Has Send to Telegram</h1>"

def send_to_telegram(messages):
  URL = "https://api.telegram.org/bot5081508998:AAGf-rPpts71oaXRu4eBRZZYVVHJWgsBojQ/sendMessage"
  message= messages
  PARAMS = {'chat_id':'-640350956','text':message}
  requests.get(url = URL, params = PARAMS)

@app.route('/bnbsdtperp_momentum_up',methods=['POST'])
def bnbusdtperp_momentum_up():
  data = json.loads(request.data)
  open = data['open']
  close = data['close']
  if(open > close):
    send_to_telegram("[BNBUSDTPERP] MOMENTUM DOWN ")
  else:
    send_to_telegram("[BNBUSDTPERP] MOMENTUM UP ")
  return"<h1>BNBUSDTPERP Momentum Up</h1>"

