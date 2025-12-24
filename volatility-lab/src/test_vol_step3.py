from data_loader import load_ohlc_data
from volatility import (
    close_to_close_volatility,
    parkinson_volatility,
    garman_klass_volatility,
    rogers_satchell_volatility,
)

df = load_ohlc_data("SPY", start="2023-01-01")

c2c = close_to_close_volatility(df, price_col="Adj Close", windows=[20, 60, 120])
park = parkinson_volatility(df, windows=[20, 60, 120])
gk = garman_klass_volatility(df, windows=[20, 60, 120])
rs = rogers_satchell_volatility(df, windows=[20, 60, 120])

# merge all
all_vol = c2c.join(park).join(gk).join(rs)

print(all_vol.tail(5))
print("\nLatest values (transposed):")
print(all_vol.dropna().tail(1).T)
