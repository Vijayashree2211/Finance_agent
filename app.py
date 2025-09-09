import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import ta
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# Load OpenRouter API Key

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7
)


# Helper Functions

def fetch_stock_data(ticker: str, period="6mo", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df

def add_indicators(df):
    df["SMA50"] = df["Close"].rolling(window=50).mean()
    df["SMA200"] = df["Close"].rolling(window=200).mean()
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    return df

def plot_price_with_sma(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["Close"], label="Close Price")
    ax.plot(df.index, df["SMA50"], label="SMA50")
    ax.plot(df.index, df["SMA200"], label="SMA200")
    ax.legend()
    ax.set_title("Price with SMA Overlays")
    return fig

def plot_rsi(df):
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(df.index, df["RSI"], label="RSI", color="purple")
    ax.axhline(70, linestyle="--", color="red")
    ax.axhline(30, linestyle="--", color="green")
    ax.set_title("Relative Strength Index (RSI)")
    return fig

def ask_financial_agent(user_query: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a financial assistant that explains stocks, mutual funds, indicators, and trading signals."),
        ("user", "{question}")
    ])
    chain = prompt | llm
    response = chain.invoke({"question": user_query})
    return response.content

def generate_trade_signal(df, rsi_buy=30, rsi_sell=70):
    """
    Generate Buy/Sell/Hold based on SMA crossover and RSI.
    - If SMA50 > SMA200 and RSI not overbought → Buy
    - If SMA50 < SMA200 and RSI not oversold → Sell
    - Otherwise → Hold
    """
    df = df.dropna(subset=["SMA50", "SMA200", "RSI"])
    if df.empty:
        return "Not enough data"

    latest = df.iloc[-1]

    # SMA crossover logic
    if latest["SMA50"] > latest["SMA200"]:
        ma_signal = "Buy"
    elif latest["SMA50"] < latest["SMA200"]:
        ma_signal = "Sell"
    else:
        ma_signal = "Hold"

    # RSI check
    if latest["RSI"] > rsi_sell:
        rsi_signal = "Sell"
    elif latest["RSI"] < rsi_buy:
        rsi_signal = "Buy"
    else:
        rsi_signal = "Hold"

    # Refined combination logic
    if ma_signal == "Buy" and rsi_signal != "Sell":
        return "Buy"
    elif ma_signal == "Sell" and rsi_signal != "Buy":
        return "Sell"
    else:
        return "Hold"



# Streamlit UI
st.set_page_config(
    page_title="FinSight",
    page_icon="💠",
    layout="wide"
)

# ==========================
# Sidebar Navigation
# ==========================
st.sidebar.title("💠 FinSight")
st.sidebar.markdown("Your AI-powered financial dashboard")

menu = st.sidebar.radio(
    "Navigate",
    ["📈 Stock Analysis", "💹 Trade Signals", "⚡ InvestiChat"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Enter valid stock tickers like **AAPL**, **MSFT**, **INFY.BO**")

# ==========================
# Stock Analysis
# ==========================
if menu == "📈 Stock Analysis":
    st.title("📈 Stock Analysis")

    ticker = st.text_input("Enter Stock Ticker:", "AAPL")

    if ticker:
        df = fetch_stock_data(ticker)
        if not df.empty:
            df = add_indicators(df)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Price Chart with SMA")
                st.pyplot(plot_price_with_sma(df))

            with col2:
                st.subheader("RSI Chart")
                st.pyplot(plot_rsi(df))
        else:
            st.warning("⚠️ No data found for this ticker.")


# ==========================
# Trade Signals
# ==========================
elif menu == "💹 Trade Signals":
    st.title("💹 Buy / Sell / Hold Signal")

    portfolio_tickers = st.text_input(
        "Enter tickers for analysis (comma separated):", 
        "AAPL, MSFT, GOOGL"
    )

    st.markdown("### ⚙️ RSI Threshold Settings")
    col1, col2 = st.columns(2)

    with col1:
        rsi_buy = st.slider("RSI Oversold Threshold (Buy)", 10, 50, 30)
    with col2:
        rsi_sell = st.slider("RSI Overbought Threshold (Sell)", 50, 90, 70)

    if st.button("🚀 Get Trade Signals"):
        tickers = [t.strip() for t in portfolio_tickers.split(",")]
        for ticker in tickers:
            df = fetch_stock_data(ticker, period="1y")
            if not df.empty:
                df = add_indicators(df)
                signal = generate_trade_signal(df, rsi_buy, rsi_sell)
                st.success(f"**{ticker}** → {signal}")
            else:
                st.warning(f"⚠️ No data found for {ticker}.")


# ==========================
# InvestiChat
# ==========================
elif menu == "⚡ InvestiChat":
    st.title("⚡ InvestiChat - Your Financial Assistant")

    user_query = st.text_area(
        "💬 Ask me anything about finance:",
        placeholder="e.g., What is SMA50? Explain Sharpe Ratio."
    )

    if st.button("Ask AI 💡") and user_query:
        with st.spinner("Thinking... 🤖"):
            response = ask_financial_agent(user_query)
            st.markdown("### 📢 Response")
            st.success(response)