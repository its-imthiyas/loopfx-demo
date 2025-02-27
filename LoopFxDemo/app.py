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

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log current working directory and sys.path for debugging
logger.info("Current Working Directory: %s", os.getcwd())
logger.info("sys.path: %s", sys.path)

# Add the parent directory of LoopFxDemo to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__)
# Load configuration into the Flask app
app.config.from_object(Config)

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Home page route that calls the same function with a default pair and period
@app.route('/', defaults={'pair': 'EURUSD', 'period': 7})
@app.route('/home', defaults={'pair': 'EURUSD', 'period': 7})
@app.route('/home/<pair>/<int:period>') # Dynamic route that accepts a currency pair and period
def home(pair, period):
    # Render the home page with the candlestick chart.
    logger.info("Initializing home route")
    data = []  # Initialize the data variable as an empty list
    graph_json = None
    message = None
    try:
        # Fetch data from the backend API
        data = fetch_data_from_api(pair, period)
        graph_json= getGraphJson(data, pair, period)
        logger.info(f"Generated graph JSON: {graph_json}")
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        graph_json = None
        message = "An error occurred while fetching data. Please try again later."
    
    # Render the data in the template
    return render_template('home.html', graph_json=graph_json, data=data, currency=pair, period=period, message=message)


def fetch_data_from_api(pair, period):
    # Fetch data from the backend API.
    api_url = f"{app.config['BACKEND_API_URL']}/currency_prices_by_pair_and_period/{pair}/{period}"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()
    print("API response:", data)
    logger.info(f"API response: {data}")
    return data

def getGraphJson(data, pair, period):
    # Create a DataFrame
    if isinstance(data, dict):
            fxdata_df = pd.DataFrame([data])
    else:
            fxdata_df = pd.DataFrame(data)
        
    if 'time' in fxdata_df.columns:
            
        fxdata_df['time'] = pd.to_datetime(fxdata_df['time'], utc=True).dt.tz_convert('UTC').dt.tz_localize(None)
        
        # Calculate the 20-period SMA and EMA
        fxdata_df['SMA20'] = fxdata_df['close'].rolling(window=20).mean()
        fxdata_df['EMA20'] = fxdata_df['close'].ewm(span=20, adjust=False).mean()
                
        # Calculate Bollinger Bands
        fxdata_df['std'] = fxdata_df['close'].rolling(window=20).std()
        fxdata_df['UpperBand'] = fxdata_df['SMA20'] + (fxdata_df['std'] * 2)
        fxdata_df['LowerBand'] = fxdata_df['SMA20'] - (fxdata_df['std'] * 2)
        
        # Create a candlestick chart using Plotly
        chart_figure = go.Figure()

        chart_figure.add_trace(go.Candlestick(
                    x=fxdata_df['time'],
                    open=fxdata_df['open'],
                    high=fxdata_df['high'],
                    low=fxdata_df['low'],
                    close=fxdata_df['close'],
                    name='Price',
                    increasing_line_color='green',
                    decreasing_line_color='red'
                ))

        # SMA20
        chart_figure.add_trace(go.Scatter(
                    x=fxdata_df['time'],
                    y=fxdata_df['SMA20'],
                    mode='lines',
                    line=dict(color='#2ca02c', width=2),
                    name='SMA20'
                ))

        # EMA20
        chart_figure.add_trace(go.Scatter(
                    x=fxdata_df['time'],
                    y=fxdata_df['EMA20'],
                    mode='lines',
                    line=dict(color='#ff7f0e', width=2),
                    name='EMA20'
                ))

        # Upper Band
        chart_figure.add_trace(go.Scatter(
                    x=fxdata_df['time'],
                    y=fxdata_df['UpperBand'],
                    mode='lines',
                    line=dict(color='#1f77b4', dash='solid', width=2),
                    name='Upper Bollinger Band',
                    #yaxis='y2',
                    opacity=0.7
                ))

        # Lower Band with fill
        chart_figure.add_trace(go.Scatter(
                    x=fxdata_df['time'],
                    y=fxdata_df['LowerBand'],
                    mode='lines',
                    line=dict(color='#1f77b4', dash='solid', width=2),
                    fill='tonexty',
                    fillcolor='rgba(31,119,180,0.2)',
                    name='Lower Bollinger Band',
                    #yaxis='y2',
                    opacity=0.7
                ))

        # Layout updates: template, margin, axes, interactive legend
        chart_figure.update_layout(
                    title=f'Candlestick Chart for {pair} - {period} days',
                    xaxis_title='Time',
                    yaxis_title='Price',
                    template='plotly_white',
                    margin=dict(l=50, r=50, b=80, t=80),
                    xaxis=dict(
                        type='date',
                        tickformat='%b %d %H:%M'
                    ),
                    #yaxis2=dict(
                    #    title='Bollinger Bands',
                    #    overlaying='y',
                    #    side='right'
                    #),
                    legend=dict(
                        itemclick='toggle',
                        itemdoubleclick='toggleothers'
                    )
                )

        # Convert the chart to JSON for rendering
        graph_json = chart_figure.to_json()
        print(graph_json)
        logger.info("Chart JSON generated")
        return graph_json
    else:
            message = "No 'time' column in the data."
            logger.warning(message)
            return None


# API endpoint to get chart data for a currency pair and period, which only returns JSON data to be used in the frontend (Using Ajax).
@app.route('/api/chart-data/<pair>/<int:period>', methods=['GET'])
def chart_data(pair, period):
    # Fetch data from the backend API
    data = fetch_data_from_api(pair, period)
    graph_json= getGraphJson(data, pair, period)
    logger.info(f"Generated graph JSON2: {graph_json}")
    return jsonify(graph_json)



# Function to fetch live currency rates from Yahoo Finance
def fetch_live_rates():
    tickers = {
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "EURGBP": "EURGBP=X"
    }
    live_data = {}
    for pair, ticker in tickers.items():
        try:
            fxdata_df = yf.download(ticker, period="1d", interval="1m")
            logger.info(f"Fetched data for {ticker}:\n{fxdata_df.tail()}")
            if not fxdata_df.empty:
                live_data[pair] = round(float(fxdata_df["Close"].iloc[-1]), 3)
            else:
                live_data[pair] = "N/A"
        except Exception as e:
            logger.error(f"Error fetching live rates for {pair}: {e}")
            live_data[pair] = "Error"
    return live_data


# API endpoint to get live currency rates
@app.route('/api/live-rates')
def live_rates():
    rates = fetch_live_rates()
    return jsonify(rates)



if __name__ == '__main__':
    logger.info("App configuration:")
    for key, value in app.config.items():
        print(f"{key}: {value}")
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])