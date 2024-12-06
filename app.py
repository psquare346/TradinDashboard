class TradingStrategy:
    def __init__(self):
        """Initialize default parameters"""
        self.default_params = {
            'short_ma': 20,
            'long_ma': 50,
            'rsi_period': 14,
            'stop_loss': 2.0,
            'take_profit': 5.0
        }
        
    def get_data(self, ticker, start_date, end_date):
        """Download stock data"""
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            return data
        except Exception as e:
            st.error(f"Error downloading data: {str(e)}")
            return None

    def calculate_indicators(self, data, short_ma, long_ma, rsi_period):
        """Calculate technical indicators"""
        signals = pd.DataFrame(index=data.index)
        
        # Calculate Moving Averages
        signals['SMA_short'] = data['Close'].rolling(window=short_ma).mean()
        signals['SMA_long'] = data['Close'].rolling(window=long_ma).mean()
        
        # Calculate RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        signals['RSI'] = 100 - (100 / (1 + rs))
        
        return signals
