from data_loader import load_ohlc_data
from volatility import close_to_close_volatility

df = load_ohlc_data("SPY", start="2023-01-01")
vol_df = close_to_close_volatility(df, price_col="Adj Close", windows=[20, 60, 120])

print(vol_df.tail(5))
print("\nLatest values (transposed):")
print(vol_df.dropna().tail(1).T)
