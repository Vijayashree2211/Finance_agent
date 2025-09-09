# FinSight 💠

**FinSight** is an AI-powered financial dashboard built with **Streamlit**. It provides interactive **stock analysis**, **trade signals**, and a conversational **financial assistant** using LLMs for intelligent insights.  

> **Disclaimer:** This tool is **for educational purposes only**. It does **not provide financial advice**. Use it to learn about stock analysis, indicators, and AI-driven insights.

---

## Features

### 📈 Stock Analysis
- Fetch historical stock data using **Yahoo Finance**.
- Visualize price charts with **Simple Moving Averages (SMA50, SMA200)**.
- Display **Relative Strength Index (RSI)** charts for momentum analysis.

### 💹 Trade Signals
- Generate Buy/Sell/Hold signals based on:
  - **SMA crossover strategy**:
    - **SMA50**: Average closing price over the last 50 days (short-term trend).  
    - **SMA200**: Average closing price over the last 200 days (long-term trend).  
    - **Signal:**  
      - SMA50 crosses above SMA200 → bullish trend → **Buy**  
      - SMA50 crosses below SMA200 → bearish trend → **Sell**
  - **RSI (Relative Strength Index)**:
    - Measures stock momentum (0–100).  
    - RSI < 30 → Oversold → possible **Buy** signal.  
    - RSI > 70 → Overbought → possible **Sell** signal.  

### ⚡ InvestiChat
- Conversational AI financial assistant powered by **LangChain + OpenRouter GPT model**.
- Answers questions about stocks, mutual funds, technical indicators, and trading strategies.

---

## Libraries Used

- **Streamlit**: For building the interactive web UI.  
- **yfinance**: To fetch historical stock price data.  
- **pandas**: Data manipulation and analysis.  
- **matplotlib**: Visualization of price charts and RSI.  
- **ta (Technical Analysis)**: Computes RSI and other financial indicators.  
- **dotenv**: Load environment variables for API keys.  
- **langchain_openai**: Integrates LLMs for natural language processing and chat.  

### LLM Integration
- **Model Used:** `openai/gpt-oss-20b:free` via **OpenRouter** API.  
- **About GPT-OSS-20B:** GPT-OSS-20B is a large open-source AI model that can understand questions and generate human-like answers. In this app, it helps explain financial terms, stock indicators, and trading concepts in simple language.



)
