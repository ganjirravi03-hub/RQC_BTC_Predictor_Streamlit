import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

# --- Configuration ---
SYMBOL = "BTCUSDT"
INTERVAL = "1m"
LIMIT = 120
REFRESH_SECONDS = 10
# Using the FAPI endpoint which is generally more stable than the Spot API on cloud hosts
BASE_URL = "https://fapi.binance.com/fapi/v1/klines"
# --- Data Fetching ---
def get_binance_klines():
    """Fetches klines data from Binance API."""
    params = {
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'limit': LIMIT
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        data = response.json()
        
        if not data:
            st.error("Error loading Binance data: API returned empty data.")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=[
            'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 
            'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 
            'Taker buy quote asset volume', 'Ignore'
        ])
        
        # Convert necessary columns to numeric
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        
        return df

    except requests.exceptions.HTTPError as errh:
        st.error(f"Error loading Binance data: Binance API Request Error: {errh}. Check API connection.")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error loading Binance data: Connection Error: {errc}. Check network or firewall.")
    except requests.exceptions.Timeout as errt:
        st.error(f"Error loading Binance data: Timeout Error: {errt}. API request took too long.")
    except requests.exceptions.RequestException as err:
        st.error(f"Error loading Binance data: An unexpected error occurred: {err}.")
    except Exception as e:
        st.error(f"Error loading Binance data: General error: {e}")
        
    return None
      # --- LSTM Model (Simple Placeholder) ---
def train_and_predict(df):
    """Placeholder for LSTM training and prediction logic."""
    data = df['Close'].values.reshape(-1, 1)
    
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Create training data
    training_data_len = int(np.ceil(len(scaled_data) * 0.95))
    train_data = scaled_data[0:training_data_len, :]
    
    # Prepare X_train and y_train (simplistic example)
    x_train, y_train = [], []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
    
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    # Build LSTM Model (simple structure)
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Train the model (simplified, should be done outside the main loop for real app)
    # model.fit(x_train, y_train, batch_size=1, epochs=1) 
    
    # --- Prediction (on the latest data) ---
    test_data = scaled_data[training_data_len - 60:, :]
    X_test = []
    X_test.append(test_data[-60:, 0]) # Last 60 points for prediction
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    
    # Use the model to predict (since we didn't train, this is dummy)
    # For a placeholder: just return a simple moving average change
    last_close = df['Close'].iloc[-1]
    avg_change = df['Close'].diff().tail(10).mean()
    
    # Simple Prediction Logic
    if avg_change > 0.05:
        prediction = "BUY (Strong Signal)"
    elif avg_change < -0.05:
        prediction = "SELL (Strong Signal)"
    else:
        prediction = "HOLD (Neutral)"
        
    return prediction, last_close
  # --- Streamlit App Layout ---
def run_app():
    st.title(f"⚡ RQC BTC Predictor LIVE")
    st.subheader(f"Real-time {SYMBOL} Data & Prediction")

    df = get_binance_klines()

    if df is not None:
        latest_close = df['Close'].iloc[-1]
        
        # --- Prediction ---
        prediction, last_close = train_and_predict(df)
        
        # --- Metrics Display ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="Current Price (USDT)", 
                      value=f"{latest_close:.2f}", 
                      delta=f"{df['Close'].diff().iloc[-1]:.2f}",
                      delta_color="normal")
        
        with col2:
            st.metric(label="Next 1 Min Prediction", 
                      value=prediction, 
                      delta="Based on 120 Mins Data", 
                      delta_color="off")

        # --- Candlestick Chart ---
        fig = go.Figure(data=[go.Candlestick(
            x=df['Close time'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )])
        
        fig.update_layout(title=f'{SYMBOL} Candlestick Chart (1m)', 
                          xaxis_title="Time", 
                          yaxis_title="Price (USDT)",
                          height=500,
                          xaxis_rangeslider_visible=False)
        
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Could not fetch data from Binance API. The error is shown above.")
          # --- Auto-refresh ---
    st.info(f"Auto-refresh every {REFRESH_SECONDS} seconds.")
    time.sleep(REFRESH_SECONDS)
    st.rerun()


if __name__ == "__main__":
    run_app()
  
