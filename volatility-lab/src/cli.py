import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import load_ohlc_data
from src.volatility import (
    close_to_close_volatility,
    parkinson_volatility,
    garman_klass_volatility,
    rogers_satchell_volatility,
)
from src.event_study import load_event_dates, pre_post_event_change, summarize_changes

def ensure_reports_dir() -> Path:
    p = Path("reports")
    p.mkdir(parents=True, exist_ok=True)
    return p


def build_vol_panel(df: pd.DataFrame, windows=(20, 60, 120)) -> pd.DataFrame:
    c2c = close_to_close_volatility(df, price_col="Adj Close", windows=list(windows))
    park = parkinson_volatility(df, windows=list(windows))
    gk = garman_klass_volatility(df, windows=list(windows))
    rs = rogers_satchell_volatility(df, windows=list(windows))
    panel = c2c.join(park).join(gk).join(rs)
    return panel


def run_event_comparison(
    vol_panel: pd.DataFrame,
    event_file: str,
    event_name: str,
    pre: int,
    post: int,
    metrics: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    events = load_event_dates(event_file)

    # per-event rows for each metric
    all_rows = []
    summaries = []

    for m in metrics:
        if m not in vol_panel.columns:
            continue

        rows = pre_post_event_change(vol_panel[m], events, pre=pre, post=post)
        if rows.empty:
            continue

        rows.insert(0, "event_name", event_name)
        rows.insert(1, "metric", m)
        all_rows.append(rows)

        summary = summarize_changes(rows)
        summary.insert(0, "event_name", event_name)
        summary.insert(1, "metric", m)
        summary.insert(2, "pre", pre)
        summary.insert(3, "post", post)
        summaries.append(summary)

    rows_df = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    summary_df = pd.concat(summaries, ignore_index=True) if summaries else pd.DataFrame()

    # ranking by avg_pct_change (higher = more reactive)
    ranking_df = summary_df.sort_values(by="avg_pct_change", ascending=False) if not summary_df.empty else pd.DataFrame()

    return rows_df, summary_df, ranking_df


def save_plot(vol_panel: pd.DataFrame, ticker: str, out_path: Path, plot_cols: list[str]):
    # Only plot cols that exist + have non-null values
    cols = [c for c in plot_cols if c in vol_panel.columns]
    plot_df = vol_panel[cols].dropna()

    if plot_df.empty:
        return

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_df.plot(ax=ax)
    ax.set_title(f"{ticker} Volatility Estimates (Annualized)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description="Volatility Lab: OHLC volatility + macro event study")
    ap.add_argument("--ticker", required=True, help="Ticker (e.g., SPY, QQQ, AAPL, BTC-USD)")
    ap.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    ap.add_argument("--end", default=None, help="End date YYYY-MM-DD (optional)")
    ap.add_argument("--windows", default="20,60,120", help="Rolling windows, comma-separated")
    ap.add_argument("--events", default=None, help="Event CSV path (must have 'date' column)")
    ap.add_argument("--event_name", default="EVENT", help="Label for events (CPI/FOMC/etc.)")
    ap.add_argument("--pre", type=int, default=20, help="Pre-event window length (trading days)")
    ap.add_argument("--post", type=int, default=20, help="Post-event window length (trading days)")
    ap.add_argument("--make_plot", action="store_true", help="Save a plot to reports/")
    args = ap.parse_args()

    windows = [int(x.strip()) for x in args.windows.split(",") if x.strip()]

    reports = ensure_reports_dir()

    df = load_ohlc_data(args.ticker, start=args.start, end=args.end)
    vol_panel = build_vol_panel(df, windows=windows)

    # Save vol panel
    vol_out = reports / "vol_panel.csv"
    vol_panel.to_csv(vol_out)
    print(f"Saved vol panel: {vol_out}")

    # Optional plot
    if args.make_plot:
        plot_out = reports / "vol_plot.png"
        save_plot(
            vol_panel,
            args.ticker,
            plot_out,
            plot_cols=[f"c2c_{windows[0]}", f"park_{windows[0]}", f"gk_{windows[0]}", f"rs_{windows[0]}"],
        )
        print(f"Saved plot: {plot_out}")

    # Event study if provided
    if args.events:
        metrics = []
        for w in windows:
            metrics += [f"c2c_{w}", f"park_{w}", f"gk_{w}", f"rs_{w}"]

        rows_df, summary_df, ranking_df = run_event_comparison(
            vol_panel=vol_panel,
            event_file=args.events,
            event_name=args.event_name,
            pre=args.pre,
            post=args.post,
            metrics=metrics,
        )

        rows_out = reports / "event_rows.csv"
        summary_out = reports / "event_summary.csv"
        rank_out = reports / "estimator_ranking.csv"

        rows_df.to_csv(rows_out, index=False)
        summary_df.to_csv(summary_out, index=False)
        ranking_df.to_csv(rank_out, index=False)

        print(f"Saved event rows: {rows_out}")
        print(f"Saved event summary: {summary_out}")
        print(f"Saved estimator ranking: {rank_out}")

        if not ranking_df.empty:
            print("\nTop estimator reactions (by avg_pct_change):")
            print(ranking_df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
