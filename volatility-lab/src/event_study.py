import pandas as pd


def load_event_dates(csv_path: str) -> pd.DatetimeIndex:
    df = pd.read_csv(csv_path)
    if "date" not in df.columns:
        raise ValueError("CSV must have a 'date' column")
    dates = pd.to_datetime(df["date"], errors="coerce").dropna()
    return pd.DatetimeIndex(dates).normalize()


def match_event_to_trading_day(trading_index: pd.DatetimeIndex, event_date: pd.Timestamp):
    """
    Map an event date to the nearest trading date on/after the event date.
    """
    event_date = pd.Timestamp(event_date).normalize()
    pos = trading_index.searchsorted(event_date, side="left")
    if pos >= len(trading_index):
        return None
    return pd.Timestamp(trading_index[pos]).normalize()


def pre_post_event_change(vol_series: pd.Series, event_dates: pd.DatetimeIndex, pre: int = 20, post: int = 20):
    """
    For each event, compute:
      pre_vol  = mean(vol over [t-pre, t-1])
      post_vol = mean(vol over [t, t+post-1])
      delta    = post_vol - pre_vol
      pct      = delta/pre_vol

    Returns a DataFrame with one row per event.
    """
    vol = vol_series.dropna().sort_index()
    idx = pd.DatetimeIndex(vol.index).normalize()

    rows = []
    for d in event_dates:
        t = match_event_to_trading_day(idx, d)
        if t is None:
            continue

        t_pos = idx.get_indexer([t])[0]
        if t_pos < 0:
            continue

        pre_start = t_pos - pre
        pre_end = t_pos - 1
        post_start = t_pos
        post_end = t_pos + post - 1

        if pre_start < 0 or post_end >= len(idx):
            continue

        pre_vol = float(vol.iloc[pre_start:pre_end + 1].mean())
        post_vol = float(vol.iloc[post_start:post_end + 1].mean())
        delta = post_vol - pre_vol
        pct = None if pre_vol == 0 else (delta / pre_vol) * 100.0

        rows.append({
            "event_date": pd.Timestamp(d).date(),
            "trading_date": pd.Timestamp(t).date(),
            "pre_vol": pre_vol,
            "post_vol": post_vol,
            "delta": delta,
            "pct_change": pct,
        })

    return pd.DataFrame(rows)


def summarize_changes(changes_df: pd.DataFrame) -> pd.DataFrame:
    if changes_df.empty:
        return pd.DataFrame([{
            "n_events": 0,
            "avg_delta": None,
            "median_delta": None,
            "pct_up": None,
            "avg_pct_change": None,
            "median_pct_change": None,
        }])

    return pd.DataFrame([{
        "n_events": int(len(changes_df)),
        "avg_delta": float(changes_df["delta"].mean()),
        "median_delta": float(changes_df["delta"].median()),
        "pct_up": float((changes_df["delta"] > 0).mean() * 100.0),
        "avg_pct_change": float(pd.to_numeric(changes_df["pct_change"]).dropna().mean()),
        "median_pct_change": float(pd.to_numeric(changes_df["pct_change"]).dropna().median()),
    }])
