import yfinance as yf
import pandas as pd
import numpy as np

def download_data(ticker: str, start: str, end: str, auto_adjust: bool = True) -> pd.DataFrame:
    """Download historical stock data from Yahoo Finance."""
    data = yf.download(ticker, start=start, end=end, auto_adjust=auto_adjust)
    return data

def log_returns(prices: pd.Series) -> pd.Series:
    """Calculate log returns from adjusted close prices."""
    prices=prices.dropna()
    r=np.log(prices / prices.shift(1)).dropna()
    r.name="log_return"
    return r

def annualized_volatility(log_returns: pd.Series, trading_days: int = 252) -> float:
    """Calculate annualized volatility from log returns."""
    return log_returns.std(ddof=1) * np.sqrt(trading_days)

def simple_r_to_cc(r_simple: float) -> float:
    """Convert simple return to continuously compounded return."""
    return np.log(1 + r_simple)