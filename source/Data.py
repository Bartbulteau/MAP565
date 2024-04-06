import yfinance as yf
import pandas as pd

def get_ticker_data(ticker, start_date, time_span, reset_index=False):
    """
    :param ticker: Stock ticker
    :param start_date: Start date of the data
    :param time_span: Time span of the data
    :return: Dataframe with the daily stock data
    """

    # Get the stock data
    data = yf.download(ticker, start=start_date, end=time_span, progress=False)
    if reset_index:
        data = data.reset_index()
    return data

def get_maang_data(start_date, time_span, reset_index=False):
    """
    :param start_date: Start date of the data
    :param time_span: Time span of the data
    :return: Dataframe with the daily stock close price of the MAANG stocks
    """

    # Get the stock data
    data = get_ticker_data('MSFT', start_date, time_span, reset_index)['Close']
    data = pd.concat([data, get_ticker_data('AAPL', start_date, time_span, reset_index)['Close']], axis=1)
    data.columns = ['MSFT', 'AAPL']
    data = pd.concat([data, get_ticker_data('AMZN', start_date, time_span, reset_index)['Close']], axis=1)
    data.columns = ['MSFT', 'AAPL', 'AMZN']
    data = pd.concat([data, get_ticker_data('NFLX', start_date, time_span, reset_index)['Close']], axis=1)
    data.columns = ['MSFT', 'AAPL', 'AMZN', 'NFLX']
    data = pd.concat([data, get_ticker_data('GOOGL', start_date, time_span, reset_index)['Close']], axis=1)
    data.columns = ['MSFT', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
    return data

def get_maang_data_default(reset_index=False):
    return get_maang_data('2014-01-01', '2024-01-01', reset_index)