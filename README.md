# risk-management-in-a-nutshell

## Objective
Short description of the goal (e.g., BSM pricing, Greeks, implied vol, hedging P&L).

## Data
- Source: Yahoo Finance (via `yfinance`)
- Asset: [AAPL / NVDA / ...]
- Frequency: Daily
- Price: Auto-adjusted close (`auto_adjust=True`)

## Methodology
- Black–Scholes–Merton pricing (European call/put)
- Greeks: Delta, Gamma, Vega, Theta, Rho
- Implied volatility (numerical solver)
- (Optional) Delta-hedging backtest

## Results


## How to run
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
jupyter lab