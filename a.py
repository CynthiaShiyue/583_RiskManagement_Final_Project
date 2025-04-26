# streamlit_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── Load data ────────────────────────────────────────
hedge_plan = pd.read_csv("final_hedge_plan.csv")
hedge_plan['date'] = pd.to_datetime(hedge_plan['date'])

returns = pd.read_csv("Data/dataset1.csv")
returns['Date'] = pd.to_datetime(returns['Date'])
returns = returns.rename(columns={"Date": "date"})
returns = returns.set_index('date')
returns = returns.dropna()

# Hedge cost per day
hedge_plan['hedge_cost'] = hedge_plan['contracts_needed'] * hedge_plan['mid_price'] * 100
daily_cost = hedge_plan.groupby('date')['hedge_cost'].sum()
cost = daily_cost.reindex(returns.index, fill_value=0.0)

# Portfolio simulation
start_value = 10_000_000
unhedged = start_value * (1 + returns['Return']).cumprod()

hedged = [start_value]
for r, c in zip(returns['Return'].iloc[1:], cost.iloc[1:]):
    hedged.append((hedged[-1] - c) * (1 + r))
hedged = pd.Series(hedged, index=returns.index)

# Volatility estimation (21-day rolling window)
rolling_vol = returns['Return'].rolling(window=21).std() * np.sqrt(252)

# Simple VaR estimation
rolling_var = returns['Return'].rolling(window=21).quantile(0.05)

# ── Streamlit dashboard ──────────────────────────────
st.title("Market Risk Dashboard: QQQ Portfolio Hedging")

st.subheader("📈 Portfolio Value")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(unhedged, label='Unhedged')
ax.plot(hedged, label='Hedged')
ax.legend()
ax.set_ylabel("Portfolio Value ($)")
st.pyplot(fig)

st.subheader("📊 Risk Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Current Volatility", f"{rolling_vol.iloc[-1]:.2%}")
col2.metric("Current 5% VaR", f"{rolling_var.iloc[-1]:.2%}")
col3.metric("Total Hedge Cost", f"${cost.sum():,.0f}")

# Risk Alert
if rolling_vol.iloc[-1] > 0.20:
    st.error(f"🚨 Volatility Alert! Realized vol is {rolling_vol.iloc[-1]:.2%}")
else:
    st.success(f"✅ Volatility under control: {rolling_vol.iloc[-1]:.2%}")

st.caption("Data: QQQ Returns + QQQ Options (Delta/Gamma Hedging)")
