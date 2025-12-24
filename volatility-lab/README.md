# Volatility Lab 📈  
*A Quantitative Analysis of Volatility Estimators and Macro Event Reactions*

## Overview
Volatility is a dynamic risk metric that changes with market conditions and information flow.  
This project builds a research-style tool to compute, compare, and analyze multiple volatility estimators on financial assets and study how they react around major macroeconomic events such as **CPI releases** and **FOMC meetings**.

Unlike basic volatility calculators, this project:
- Uses **OHLC-based estimators** (not just close-to-close returns)
- Treats volatility as **time-varying**
- Applies an **event study framework** to macro announcements

---

## Key Features

### 1. Volatility Estimators
The tool computes rolling, annualized volatility using:

- **Close-to-Close Volatility** (log returns)
- **Parkinson Volatility** (High–Low range)
- **Garman–Klass Volatility** (OHLC-based)
- **Rogers–Satchell Volatility** (drift-robust OHLC estimator)

Each estimator is calculated over **20, 60, and 120 trading-day windows**.

---

### 2. Event Study Analysis
For each macro event (CPI or FOMC):

- Aligns event dates to trading days
- Computes average volatility **before vs after** the event
- Measures:
  - Absolute change
  - Percentage change
  - Frequency of volatility increase
- Ranks estimators by **reaction strength**

This allows direct comparison of how different estimators respond to macro shocks.

---

### 3. Research-Grade Design
- Modular code structure (`data_loader`, `volatility`, `event_study`)
- Command-line interface (CLI)
- Reproducible CSV outputs
- Clean separation between data, analytics, and reporting

---

## Project Structure

volatility-lab/
│
├── src/
│ ├── data_loader.py # OHLC data ingestion
│ ├── volatility.py # Volatility estimators
│ ├── event_study.py # Event study logic
│ └── cli.py # Command-line interface
│
├── data/
│ ├── events_cpi.csv
│ └── events_fomc.csv
│
├── reports/
│ ├── vol_panel.csv
│ ├── event_rows.csv
│ ├── event_summary.csv
│ ├── estimator_ranking.csv
│ └── vol_plot.png
│
├── tests/
├── README.md
└── requirements.txt

yaml
Copy code

---

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
Usage
Run CPI Event Study
bash
Copy code
python -m src.cli \
  --ticker SPY \
  --start 2023-01-01 \
  --events data/events_cpi.csv \
  --event_name CPI \
  --make_plot
Run FOMC Event Study
bash
Copy code
python -m src.cli \
  --ticker SPY \
  --start 2023-01-01 \
  --events data/events_fomc.csv \
  --event_name FOMC \
  --make_plot
Outputs are saved automatically to the reports/ directory.

Sample Findings
Short-window volatility (20-day) reacts faster to macro events than longer windows.

Close-to-close volatility captures macro repricing risk most strongly.

OHLC estimators provide smoother signals and differ in sensitivity depending on intraday range behavior.

FOMC events generate larger volatility reactions than CPI releases on average.

Why This Project Matters
This project demonstrates:

Understanding of volatility as a dynamic risk process

Knowledge of professional volatility estimators

Application of event-study methodology

Clean, reproducible research code design

It bridges computer science, financial engineering, and quantitative risk analysis.

Future Extensions
Volatility forecasting and backtesting

Regime detection (low/medium/high volatility states)

CPI surprise magnitude vs volatility response

Cross-asset and sector-level analysis

License
MIT License

yaml
Copy code

---

# PART 2 — CREATE THE GITHUB REPO & PUSH CODE

You already have a GitHub account:  
👉 **https://github.com/Dhruv12310**

## Step 1 — Initialize Git locally
From inside `volatility-lab`:

```bash
git init
git add .
git commit -m "Initial commit: volatility estimators and macro event study"