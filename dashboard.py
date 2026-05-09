import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Stock Market Data Analyzer",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("📈 Stock Market Data Analyzer")

st.markdown("""
Analyze real-time stock market data using Python,
Yahoo Finance API, and financial analytics.
""")

# -----------------------------------
# SIDEBAR INPUT
# -----------------------------------

st.sidebar.header("User Input")

ticker = st.sidebar.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime("2023-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    pd.to_datetime("2024-01-01")
)

# -----------------------------------
# FETCH DATA
# -----------------------------------

data = yf.download(
    ticker,
    start=start_date,
    end=end_date
)

# -----------------------------------
# FIX MULTI-LEVEL COLUMNS
# -----------------------------------

data.columns = data.columns.get_level_values(0)

data.columns.name = None

data.reset_index(inplace=True)

# -----------------------------------
# DAILY RETURNS
# -----------------------------------

data['Daily_Return'] = data['Close'].pct_change()

# -----------------------------------
# MOVING AVERAGES
# -----------------------------------

data['MA20'] = data['Close'].rolling(window=20).mean()

data['MA50'] = data['Close'].rolling(window=50).mean()

# -----------------------------------
# VOLATILITY
# -----------------------------------

volatility = data['Daily_Return'].std()

# -----------------------------------
# METRICS
# -----------------------------------

highest_price = data['High'].max()

lowest_price = data['Low'].min()

average_return = data['Daily_Return'].mean()

# -----------------------------------
# SHOW DATAFRAME
# -----------------------------------

st.subheader("📊 Stock Dataset")

st.dataframe(data.head())

# -----------------------------------
# METRICS DISPLAY
# -----------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Highest Price",
    f"{highest_price:.2f}"
)

col2.metric(
    "Lowest Price",
    f"{lowest_price:.2f}"
)

col3.metric(
    "Volatility",
    f"{volatility:.5f}"
)

col4.metric(
    "Average Return",
    f"{average_return:.5f}"
)

# -----------------------------------
# CLOSING PRICE CHART
# -----------------------------------

st.subheader("📈 Closing Price Trend")

fig1, ax1 = plt.subplots(figsize=(12,6))

ax1.plot(
    data['Date'],
    data['Close'],
    label='Closing Price'
)

ax1.set_title(f"{ticker} Closing Price")

ax1.set_xlabel("Date")

ax1.set_ylabel("Price")

ax1.grid(True)

st.pyplot(fig1)

# -----------------------------------
# MOVING AVERAGE CHART
# -----------------------------------

st.subheader("📉 Moving Average Analysis")

fig2, ax2 = plt.subplots(figsize=(12,6))

ax2.plot(
    data['Date'],
    data['Close'],
    label='Close Price'
)

ax2.plot(
    data['Date'],
    data['MA20'],
    label='20-Day MA'
)

ax2.plot(
    data['Date'],
    data['MA50'],
    label='50-Day MA'
)

ax2.set_title(f"{ticker} Moving Average Analysis")

ax2.set_xlabel("Date")

ax2.set_ylabel("Price")

ax2.legend()

ax2.grid(True)

st.pyplot(fig2)

# -----------------------------------
# RETURN DISTRIBUTION
# -----------------------------------

st.subheader("📊 Daily Return Distribution")

fig3, ax3 = plt.subplots(figsize=(10,5))

sns.histplot(
    data['Daily_Return'].dropna(),
    bins=50,
    kde=True,
    ax=ax3
)

ax3.set_title(f"{ticker} Daily Return Distribution")

st.pyplot(fig3)

# -----------------------------------
# FINAL INSIGHTS
# -----------------------------------

st.subheader("📋 Final Insights")

st.write(f"""
- Highest observed stock price: {highest_price:.2f}
- Lowest observed stock price: {lowest_price:.2f}
- Stock volatility: {volatility:.5f}
- Average daily return: {average_return:.5f}

Moving averages help identify market trends.
Volatility indicates investment risk level.
Daily returns measure stock performance.
""")