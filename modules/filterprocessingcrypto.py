from binance.client import Client
from binance.enums import HistoricalKlinesType
import pandas as pd

from modules.config import *
from modules.logic_process.crypto_logic import *

class FilterProcessingCrypto:
    client = None
    open, close = 0,0
    last_index = 0
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET)
        
    def GetHistoricalData(self, symbol, interval, date):
        klines = self.client.get_historical_klines(symbol, interval, date, klines_type=HistoricalKlinesType.FUTURES)
        df = pd.DataFrame(klines, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
        df.dateTime = pd.to_datetime(df.dateTime)
        df['date'] = df.dateTime.dt.strftime("%d/%m/%Y")
        df['time'] = df.dateTime.dt.strftime("%H:%M:%S")
        df['open'] = df['open'].astype(float)
        df['close'] = df['close'].astype(float)
        df['low'] = df['low'].astype(float)
        df['high'] = df['high'].astype(float)
        df['volume'] = df['volume'].astype(float)
        df = df.drop(['dateTime', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol','takerBuyQuoteVol', 'ignore'], axis=1)
        column_names = ["time", "open", "high", "low", "close", "volume"]
        df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
        df = df.reindex(columns=column_names)

        self.client.close_connection()
        return df

    def initial_dataset(self,symbol):
        hour = 60
        Date = "{} hour ago UTC".format(hour)
        symbol = symbol
        interval = Client.KLINE_INTERVAL_1HOUR
        df = self.GetHistoricalData(symbol, interval, Date)

        self.last_index = len(df) - 2
        self.open = df['open'].iloc[self.last_index]
        self.close = df['close'].iloc[self.last_index]
        
        return df

    def process_data(self,dataset,signal):
        irisan = list()
        new_dataset = list()
        for element_symbol in dataset:
            symbol = element_symbol.replace("PERP","")
            try:
                data = self.initial_dataset(symbol)
                logic = CryptoLogic(data)
                if(logic.process(signal)):
                    change = ((self.close - self.open) / self.open ) * 100
                    new_dataset.append( element_symbol + " | " + str( change.round(2) ) + "%" ) 
                else:
                    irisan.append(element_symbol)
            except:
                pass
        return [new_dataset,irisan]

    