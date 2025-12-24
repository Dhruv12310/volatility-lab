from data_loader import load_ohlc_data
from volatility import (
    close_to_close_volatility,
    parkinson_volatility,
    garman_klass_volatility,
    rogers_satchell_volatility,
)
from event_study import load_event_dates, pre_post_event_change, summarize_changes

ticker = "SPY"
start = "2023-01-01"

df = load_ohlc_data(ticker, start=start)

# compute all vols
c2c = close_to_close_volatility(df, price_col="Adj Close", windows=[20, 60, 120])
park = parkinson_volatility(df, windows=[20, 60, 120])
gk = garman_klass_volatility(df, windows=[20, 60, 120])
rs = rogers_satchell_volatility(df, windows=[20, 60, 120])

all_vol = c2c.join(park).join(gk).join(rs)

# choose event file (try CPI first)
events = load_event_dates("data/events_cpi.csv")

metrics_to_compare = [
    "c2c_20", "c2c_60",
    "park_20", "park_60",
    "gk_20", "gk_60",
    "rs_20", "rs_60",
]

results = []
for m in metrics_to_compare:
    changes = pre_post_event_change(all_vol[m], events, pre=20, post=20)
    summary = summarize_changes(changes)
    summary.insert(0, "metric", m)
    results.append(summary)

final = __import__("pandas").concat(results, ignore_index=True)
final = final.sort_values(by="avg_pct_change", ascending=False)

print(final.to_string(index=False))
