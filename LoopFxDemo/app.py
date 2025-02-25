import sys
import os
import logging
from flask import Flask, render_template, jsonify, request
import requests
import plotly.express as px
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from config import Config

# Print current working directory and sys.path for debugging
print("Current Working Directory:", os.getcwd())
print("sys.path:", sys.path)

# Add the parent directory of LoopFxDemo to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__)
# Load configuration into your Flask app
app.config.from_object(Config)

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/home', defaults={'pair': 'EURUSD', 'period': 7})
@app.route('/home/<pair>/<int:period>')
def home(pair, period):
    """Render the home page with the candlestick chart."""
    logger.info("Initializing home route")
    data = []  # Initialize the data variable as an empty list
    graph_json = None
    message = None
    try:
        # Fetch data from the backend API
        api_url = f"{app.config['BACKEND_API_URL']}/currency_prices_by_pair_and_period/{pair}/{period}"
        print(api_url)
        response = requests.get(api_url)
        data = response.json()
        print("API response:", data)
        
        # Wrap the data if needed and create a DataFrame
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)
        
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'], utc=True).dt.tz_convert('UTC').dt.tz_localize(None)
            
            # Calculate the 20-period SMA and EMA
            df['SMA20'] = df['close'].rolling(window=20).mean()
            df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
            
            # Calculate Bollinger Bands
            df['std'] = df['close'].rolling(window=20).std()
            df['UpperBand'] = df['SMA20'] + (df['std'] * 2)
            df['LowerBand'] = df['SMA20'] - (df['std'] * 2)
    
            # Create the candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price'
            )])
    
            # Add SMA and EMA traces
            fig.add_trace(go.Scatter(x=df['time'], y=df['SMA20'], mode='lines', name='SMA20'))
            fig.add_trace(go.Scatter(x=df['time'], y=df['EMA20'], mode='lines', name='EMA20'))
    
            # Add Bollinger Bands: Upper Band
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df['UpperBand'],
                mode='lines',
                line=dict(color='rgba(131, 90, 241, 1)', dash='solid'),
                name='Upper Bollinger Band',
                opacity=0.5
            ))
    
            # Add Bollinger Bands: Lower Band with fill
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df['LowerBand'],
                mode='lines',
                line=dict(color='rgba(131, 90, 241, 1)', dash='solid'),
                fill='tonexty',
                name='Lower Bollinger Band',
                fillcolor='rgba(131, 90, 241, 0.2)'  # Semi-transparent fill
            ))
    
            # Update layout with axis titles and margins
            fig.update_layout(
                title=f'Candlestick Chart for {pair} - {period} days',
                xaxis_title='Time',
                yaxis_title='Price',
                xaxis=dict(
                    type='date',
                    tickformat='%b %d %H:%M'
                ),
                margin=dict(l=50, r=50, b=80, t=80)
            )
    
            # Convert the chart to JSON for rendering
            graph_json = fig.to_json()
            print(graph_json)
            logger.info("Chart JSON generated")
        else:
            message = "No 'time' column in the data."
            logger.warning(message)
    
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        graph_json = None
        message = "An error occurred while fetching data. Please try again later."
    
    # Render the data in the template
    return render_template('home.html', graph_json=graph_json, data=data, currency=pair, period=period, message=message)


def fetch_live_rates():
    tickers = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "EURGBP": "EURGBP=X"
    }
    live_data = {}
    for pair, ticker in tickers.items():
        try:
            df = yf.download(ticker, period="1d", interval="1m")
            logger.info(f"Fetched data for {ticker}:\n{df.tail()}")
            if not df.empty:
                live_data[pair] = round(float(df["Close"].iloc[-1]), 3)
            else:
                live_data[pair] = "N/A"
        except Exception as e:
            logger.error(f"Error fetching live rates for {pair}: {e}")
            live_data[pair] = "Error"
    return live_data


@app.route('/api/live-rates')
def live_rates():
    rates = fetch_live_rates()
    return jsonify(rates)


if __name__ == '__main__':
    logger.info("App configuration:")
    for key, value in app.config.items():
        print(f"{key}: {value}")
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])