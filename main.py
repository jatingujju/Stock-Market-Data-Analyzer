from ta.momentum import RSIIndicator
import matplotlib
matplotlib.use('TkAgg')

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# STOCK DATA FETCHING
# -------------------------------

ticker = "AAPL"

print(f"\nFetching data for {ticker}...\n")

data = yf.download(
    ticker,
    start="2023-01-01",
    end="2024-01-01"
)

# -------------------------------
# FIX MULTI-LEVEL COLUMNS
# -------------------------------

data.columns = data.columns.get_level_values(0)

# Remove column axis name
data.columns.name = None

# Reset index
data.reset_index(inplace=True)

# -------------------------------
# DISPLAY DATA
# -------------------------------

print(data.head())

# -------------------------------
# SAVE CSV
# -------------------------------

data.to_csv("data/AAPL_stock_data.csv", index=False)

print("\nCSV file saved successfully!")

# -------------------------------
# DAILY RETURNS
# -------------------------------

data['Daily_Return'] = data['Close'].pct_change()

# -------------------------------
# MOVING AVERAGES
# -------------------------------

data['MA20'] = data['Close'].rolling(window=20).mean()

data['MA50'] = data['Close'].rolling(window=50).mean()

# -------------------------------
# RSI CALCULATION
# -------------------------------

rsi = RSIIndicator(close=data['Close'])

data['RSI'] = rsi.rsi()

# -------------------------------
# VOLATILITY
# -------------------------------

volatility = data['Daily_Return'].std()

print("\n========== RSI VALUES ==========")

print(data[['Date', 'Close', 'RSI']].tail())

# -------------------------------
# HIGHEST & LOWEST PRICE
# -------------------------------

highest_price = data['High'].max()

lowest_price = data['Low'].min()

# -------------------------------
# PRINT ANALYSIS SUMMARY
# -------------------------------

print("\n========== STOCK ANALYSIS ==========")

print(f"\nHighest Price : {highest_price:.2f}")

print(f"Lowest Price  : {lowest_price:.2f}")

print(f"Volatility    : {volatility:.5f}")

print(f"Average Return: {data['Daily_Return'].mean():.5f}")

# -------------------------------
# PRICE TREND CHART
# -------------------------------

plt.figure(figsize=(12,6))

plt.plot(
    data['Date'],
    data['Close'],
    label='Closing Price'
)

plt.title(f"{ticker} Closing Price Trend")

plt.xlabel("Date")

plt.ylabel("Price")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig("images/closing_price.png")

plt.show()

# -------------------------------
# MOVING AVERAGE CHART
# -------------------------------

plt.figure(figsize=(12,6))

plt.plot(
    data['Date'],
    data['Close'],
    label='Closing Price'
)

plt.plot(
    data['Date'],
    data['MA20'],
    label='20-Day Moving Average'
)

plt.plot(
    data['Date'],
    data['MA50'],
    label='50-Day Moving Average'
)

plt.title(f"{ticker} Moving Average Analysis")

plt.xlabel("Date")

plt.ylabel("Price")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig("images/moving_average.png")

plt.show()

# -------------------------------
# DAILY RETURN DISTRIBUTION
# -------------------------------

plt.figure(figsize=(10,5))

sns.histplot(
    data['Daily_Return'].dropna(),
    bins=50,
    kde=True
)

plt.title(f"{ticker} Daily Return Distribution")

plt.xlabel("Daily Return")

plt.ylabel("Frequency")

plt.grid(True)

plt.tight_layout()

plt.savefig("images/return_distribution.png")

plt.show()

# -------------------------------
# RSI VISUALIZATION
# -------------------------------

plt.figure(figsize=(12,6))

plt.plot(
    data['Date'],
    data['RSI'],
    label='RSI'
)

# Overbought Line
plt.axhline(
    70,
    color='red',
    linestyle='--',
    label='Overbought (70)'
)

# Oversold Line
plt.axhline(
    30,
    color='green',
    linestyle='--',
    label='Oversold (30)'
)

plt.title(f"{ticker} RSI Analysis")

plt.xlabel("Date")

plt.ylabel("RSI")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig("images/rsi_analysis.png")

plt.show()

# -------------------------------
# FINAL REPORT GENERATION
# -------------------------------

report = f"""
=================================
      STOCK ANALYSIS REPORT
=================================

Ticker Symbol : {ticker}

Highest Price : {highest_price:.2f}

Lowest Price  : {lowest_price:.2f}

Volatility    : {volatility:.5f}

Average Daily Return :
{data['Daily_Return'].mean():.5f}

Observations:
- Moving averages help identify trends.
- Volatility indicates stock risk.
- Daily returns show stock performance.

=================================
"""

with open("reports/stock_report.txt", "w") as file:
    file.write(report)

print("\nStock report generated successfully!")

print("\nCharts saved in images folder!")

print("\nProject execution completed successfully!")