import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


# ---------------------------
# Generate fake candles
# ---------------------------
def generate_fake_candles(current_price, candles=100):
    prices = np.linspace(current_price * 0.97, current_price * 1.03, candles)
    df = pd.DataFrame({
        "open": prices + np.random.uniform(-20, 20, candles),
        "high": prices + np.random.uniform(10, 40, candles),
        "low": prices - np.random.uniform(10, 40, candles),
        "close": prices + np.random.uniform(-20, 20, candles),
        "time": pd.date_range(end=pd.Timestamp.now(), periods=candles)
    })
    return df


# ---------------------------
# Line Chart
# ---------------------------
def get_line_chart(df):
    fig = px.line(df, x="time", y="close", title="BTC Line Chart")
    fig.update_layout(height=400)
    return fig


# ---------------------------
# Candle Chart
# ---------------------------
def get_candle_chart(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    fig.update_layout(title="BTC Candle Chart", height=450)
    return fig
  
