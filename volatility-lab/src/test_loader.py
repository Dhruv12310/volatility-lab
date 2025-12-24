from data_loader import load_ohlc_data

df = load_ohlc_data("SPY", start="2023-01-01")

print(df.head())
print("\nColumns:", df.columns)
print("\nNumber of rows:", len(df))
