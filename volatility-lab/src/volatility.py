import numpy as np
import pandas as pd

TRADING_DAYS = 252


def compute_log_returns(price_series: pd.Series) -> pd.Series:
    """
    Compute log returns: r_t = ln(P_t / P_{t-1})
    """
    return np.log(price_series / price_series.shift(1)).dropna()


def annualize_vol(daily_vol: pd.Series | float) -> pd.Series | float:
    """
    Annualize daily volatility using sqrt(252).
    """
    return daily_vol * np.sqrt(TRADING_DAYS)


def close_to_close_volatility(
    df: pd.DataFrame,
    price_col: str = "Adj Close",
    windows: list[int] = [20, 60, 120],
) -> pd.DataFrame:
    """
    Close-to-close volatility using log returns on a chosen price column.

    Returns a DataFrame with:
      - log_return
      - rolling vol columns (annualized): c2c_20, c2c_60, c2c_120
    """
    if price_col not in df.columns:
        raise ValueError(f"{price_col} not found in DataFrame columns: {df.columns.tolist()}")

    price = df[price_col].astype(float)
    r = compute_log_returns(price)

    out = pd.DataFrame(index=r.index)
    out["log_return"] = r

    for w in windows:
        out[f"c2c_{w}"] = annualize_vol(out["log_return"].rolling(w).std(ddof=1))

    return out

def _annualized_rolling_vol_from_daily_var(daily_var: pd.Series, window: int) -> pd.Series:
    """
    Convert a daily variance series into an annualized rolling volatility series:
      vol_t = sqrt(mean(var over window)) * sqrt(252)
    """
    return np.sqrt(daily_var.rolling(window).mean()) * np.sqrt(TRADING_DAYS)


def parkinson_volatility(df: pd.DataFrame, windows: list[int] = [20, 60, 120]) -> pd.DataFrame:
    """
    Parkinson volatility (uses High, Low).
    Returns annualized rolling vols: park_20, park_60, park_120
    """
    H = df["High"].astype(float)
    L = df["Low"].astype(float)

    # daily variance estimate
    daily_var = (np.log(H / L) ** 2) / (4.0 * np.log(2.0))

    out = pd.DataFrame(index=df.index)
    for w in windows:
        out[f"park_{w}"] = _annualized_rolling_vol_from_daily_var(daily_var, w)

    return out


def garman_klass_volatility(df: pd.DataFrame, windows: list[int] = [20, 60, 120]) -> pd.DataFrame:
    """
    Garman-Klass volatility (uses Open, High, Low, Close).
    Returns annualized rolling vols: gk_20, gk_60, gk_120
    """
    O = df["Open"].astype(float)
    H = df["High"].astype(float)
    L = df["Low"].astype(float)
    C = df["Close"].astype(float)

    hl = np.log(H / L)
    co = np.log(C / O)

    # daily variance estimate
    daily_var = 0.5 * (hl ** 2) - (2.0 * np.log(2.0) - 1.0) * (co ** 2)

    # numerical safety: variance shouldn't be negative, clamp small negatives to 0
    daily_var = daily_var.clip(lower=0.0)

    out = pd.DataFrame(index=df.index)
    for w in windows:
        out[f"gk_{w}"] = _annualized_rolling_vol_from_daily_var(daily_var, w)

    return out


def rogers_satchell_volatility(df: pd.DataFrame, windows: list[int] = [20, 60, 120]) -> pd.DataFrame:
    """
    Rogers-Satchell volatility (drift-robust, uses Open, High, Low, Close).
    Returns annualized rolling vols: rs_20, rs_60, rs_120
    """
    O = df["Open"].astype(float)
    H = df["High"].astype(float)
    L = df["Low"].astype(float)
    C = df["Close"].astype(float)

    ho = np.log(H / O)
    hc = np.log(H / C)
    lo = np.log(L / O)
    lc = np.log(L / C)

    # daily variance estimate
    daily_var = (ho * hc) + (lo * lc)

    # variance should be non-negative; clamp tiny negatives from floating error
    daily_var = daily_var.clip(lower=0.0)

    out = pd.DataFrame(index=df.index)
    for w in windows:
        out[f"rs_{w}"] = _annualized_rolling_vol_from_daily_var(daily_var, w)

    return out
