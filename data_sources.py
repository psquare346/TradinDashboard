from abc import ABC, abstractmethod
import pandas as pd
import yfinance as yf
import yaml
import os

class DataSourceBase(ABC):
    """Base class template for all data sources"""
    
    @abstractmethod
    def get_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Method that must be implemented by all data sources
        
        Parameters:
        ticker (str): Symbol of the stock
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        
        Returns:
        pd.DataFrame: DataFrame with columns [Open, High, Low, Close, Volume]
        """
        pass
    
    @abstractmethod
    def validate_connection(self) -> bool:
        """Test if data source connection is working"""
        pass

class YFinanceSource(DataSourceBase):
    """YFinance implementation"""
    
    def get_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            return data
        except Exception as e:
            raise Exception(f"YFinance error: {str(e)}")
    
    def validate_connection(self) -> bool:
        try:
            # Test connection by downloading a small amount of data
            test_data = yf.download("SPY", period="1d")
            return not test_data.empty
        except:
            return False

class AlphaVantageSource(DataSourceBase):
    """Alpha Vantage implementation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        # Implementation for Alpha Vantage
        # You would add the actual implementation when needed
        pass
    
    def validate_connection(self) -> bool:
        # Implementation for Alpha Vantage connection test
        pass

class DataSourceFactory:
    """Factory class to create data source instances"""
    
    @staticmethod
    def create_data_source(source_type: str, **kwargs) -> DataSourceBase:
        """
        Create a data source instance based on configuration
        
        Parameters:
        source_type (str): Type of data source ('yfinance', 'alphavantage', etc.)
        **kwargs: Additional parameters needed for the data source
        
        Returns:
        DataSourceBase: Instance of the specified data source
        """
        if source_type.lower() == 'yfinance':
            return YFinanceSource()
        elif source_type.lower() == 'alphavantage':
            api_key = kwargs.get('api_key')
            if not api_key:
                raise ValueError("API key required for Alpha Vantage")
            return AlphaVantageSource(api_key)
        else:
            raise ValueError(f"Unknown data source type: {source_type}")

# Configuration handling
def load_config(config_file: str = 'config.yaml') -> dict:
    """Load configuration from yaml file"""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    return {}

def get_data_source(config_file: str = 'config.yaml') -> DataSourceBase:
    """Create data source from configuration"""
    config = load_config(config_file)
    source_config = config.get('data_source', {'provider': 'yfinance'})
    
    return DataSourceFactory.create_data_source(
        source_config['provider'],
        **source_config.get('parameters', {})
    )
