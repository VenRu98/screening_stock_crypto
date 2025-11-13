import pandas as pd
from yahooquery import Ticker
from modules.config import *
from modules.logic_process.stock_logic import *
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


class FilterProcessingStock:
    volume, close, open = 0, 0, 0
    highs, lows = [], []
    last_index = 0

    def GetHistoricalData(self, symbol, interval, date):
        t = Ticker("{}.JK".format(symbol))
        df = t.history(period=date, interval=interval)
        # reset MultiIndex menjadi kolom biasa
        if isinstance(df.index, pd.MultiIndex):
            df = df.reset_index()
        df = df.rename({'Date': 'date', 'Open': 'open', 'High': 'high',
                       'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, axis=1)
        df['date'] = pd.to_datetime(df['date'], utc=True).dt.tz_convert(None)
        df['open'] = df['open'].astype(float)
        df['close'] = df['close'].astype(float)
        df['low'] = df['low'].astype(float)
        df['high'] = df['high'].astype(float)
        df['volume'] = df['volume'].astype(float) 
        df = df.set_index('date')
        return df

    def initial_dataset(self, symbol):
        day = 60
        Date = "{}d".format(day)
        symbol = symbol
        interval = "1d"
        df = self.GetHistoricalData(symbol, interval, Date)

        self.last_index = len(df) - 1
        self.volume = df['volume'].iloc[self.last_index]
        self.close = df['close'].iloc[self.last_index]
        self.open = df['open'].iloc[self.last_index]
        return df

    def process_data(self, dataset, signal):
        irisan = list()
        new_dataset = list()

        with ThreadPoolExecutor(max_workers=1) as ex:
            futures = [
                ex.submit(
                    self.__generate_data_stock, symbol, signal)
                for symbol
                in dataset
            ]
            for future in as_completed(futures, timeout=120):
                try:
                    result = future.result()
                    [dataset, is_new] = result
                    if (is_new):
                        new_dataset.append(dataset)
                    else:
                        irisan.append(dataset)
                except Exception as error:
                    print("ERROR Future!:", error)
                    pass
        return [new_dataset, irisan]

    # Private
    def __stoch(self, close, high, low, length):
        return 100 * (close - low.rolling(length).min()) / (high.rolling(length).max() - low.rolling(length).min())

    def __generate_data_stock(self, symbol, signal):
        result = ""
        is_new = False
        symbol = symbol
        data = self.initial_dataset(symbol)
        logic = StockLogic(data, self.last_index)
        if (logic.process(signal)):
            change = ((self.close - self.open) / self.open) * 100
            result = symbol + " | " + str(change.round(2)) + "% | " + str(
                (self.volume // 1000000) / 10) + "M | " + str(self.close)
            is_new = True
        else:
            result = symbol

        return [result, is_new]
