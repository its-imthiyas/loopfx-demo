from flask import Flask, render_template, jsonify
import requests
import plotly.express as px
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

# Define the backend API URL
BACKEND_API_URL = "http://127.0.0.1:5000/api"



@app.route('/')
def index():
    # Fetch data from the backend API
    response = requests.get(f"{BACKEND_API_URL}/currency_prices/10")
    data = response.json()
    
    # Render the data in the template
    return render_template('index.html', data=data)


@app.route('/home')
def home():
    # Fetch data from the backend API
    # data = fetch_data_from_api(f"{BACKEND_API_URL}/currency_prices/200")
    response = requests.get(f"{BACKEND_API_URL}/currency_prices_by_pair/EURUSD")
    data = response.json()
    
    if data:
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])
        df['time'] = df['time'].dt.tz_localize(None)
        
        # Calculate moving averages over a 20-period window
        df['SMA20'] = df['close'].rolling(window=20).mean()
        df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
        
        fig = px.line(df, x='time', y='close', title='Currency Prices Over Time')
        graph_json = fig.to_json()
    else:
        graph_json = None
    
    
      # Create the candlestick chart
    fig2 = go.Figure(data=[go.Candlestick(x=df['time'],
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])
    
    # Overlay the 20-period SMA and EMA
    fig2.add_trace(go.Scatter(x=df['time'], y=df['SMA20'], mode='lines', name='SMA20'))
    fig2.add_trace(go.Scatter(x=df['time'], y=df['EMA20'], mode='lines', name='EMA20'))
    
    fig2.update_layout(title=f'Candlestick Chart for EURUSD',
                      xaxis_title='Time',
                      yaxis_title='Price',
                      xaxis=dict(
            type='date',
            tickformat='%b %d %H:%M'
        ))

    
    # Convert the chart to JSON
    graph_json2 = fig2.to_json()
    
    # Render the data in the template
    return render_template('home.html', graph_json=graph_json, graph_json2=graph_json2, data=data)


@app.route('/currency/<pair>')
def currency(pair):
    # Fetch data for a specific currency pair from the backend API
    response = requests.get(f"{BACKEND_API_URL}/currency_prices_by_pair/{pair}")
    data = response.json()
    
    # Render the data in the template
    return render_template('currency.html', data=data, pair=pair)

@app.route('/period/<int:period>')
def period(period):
    # Fetch data for a specific period from the backend API
    response = requests.get(f"{BACKEND_API_URL}/currency_prices_by_period/{period}")
    data = response.json()
    
    # Render the data in the template
    return render_template('period.html', data=data, period=period)


# @app.route('/pair/<pair>')
# def pair(pair):
#     # Fetch data for a specific currency pair from the backend API
#     data = fetch_data_from_api(f"{BACKEND_API_URL}/currency_prices_by_pair/{pair}")
    
#     # Convert the data to a DataFrame
#     df = pd.DataFrame(data)
    
#     # Create the candlestick chart
#     fig = go.Figure(data=[go.Candlestick(x=df['time'],
#                                          open=df['open'],
#                                          high=df['high'],
#                                          low=df['low'],
#                                          close=df['close'])])
#     fig.update_layout(title=f'Candlestick Chart for {pair}',
#                       xaxis_title='Time',
#                       yaxis_title='Price')
    
#     # Convert the chart to JSON
#     graph_json = fig.to_json()
    
#     # Render the data in the template
#     return render_template('pair.html', graph_json=graph_json, pair=pair)

if __name__ == '__main__':
    app.run(port=8000, debug=True)