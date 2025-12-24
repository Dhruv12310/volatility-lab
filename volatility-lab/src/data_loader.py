import pandas as pd
import yfinance as yf


def load_ohlc_data(
    ticker: str,
    start: str,
    end: str | None = None,
) -> pd.DataFrame:
    """
    Load daily OHLC data for a given ticker.

    Returns a DataFrame with:
      - index: DatetimeIndex (trading days)
      - columns: Open, High, Low, Close, Adj Close, Volume
    """

    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for ticker {ticker}")

    # yfinance sometimes returns multi-index columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    required_cols = ["Open", "High", "Low", "Close"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required OHLC column: {col}")

    df = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
    df = df.dropna()
    df.index = pd.to_datetime(df.index)

    return df
