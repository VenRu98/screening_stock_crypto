import yfinance as yf

class FilterProcessingStock:
    volume, close, open = 0,0,0
    highs, lows = [] , []
    last_index = 0
    def GetHistoricalData(self, symbol, interval, date):
        df = yf.download( tickers="{}.JK".format(symbol) , period=date, interval=interval)
        df = df.drop(['Adj Close'], axis=1)
        df = df.rename({'Date':'date','Open': 'open', 'High': 'high', 'Low':'low','Close':'close','Volume':'volume'}, axis=1)
        df['open'] = df['open'].astype(float)
        df['close'] = df['close'].astype(float)
        df['low'] = df['low'].astype(float)
        df['high'] = df['high'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return df

    def initial_dataset(self,symbol):
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

    
    def process_data(self,dataset,signal):
        irisan = list()
        new_dataset = list()
        for element_symbol in dataset:
            symbol = element_symbol
            data = self.initial_dataset(symbol)
            if():

                change = ((self.close - self.open) / self.open ) * 100
                new_dataset.append( symbol + " | " + str( change.round(2) ) + "% | " + str(  (self.volume // 1000000) / 10  ) + "M | " + str(self.close) ) 
            else:
                irisan.append(symbol)
        return [new_dataset,irisan]

    # Private
    def __stoch(self, close, high, low, length):
        return 100 * (close - low.rolling(length).min())  / (high.rolling(length).max() - low.rolling(length).min())