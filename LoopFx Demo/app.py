from flask import Flask, render_template, jsonify
import requests

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

# @app.route('/home')
# def home():
#     # Fetch data from the backend API
#     response = requests.get(f"{BACKEND_API_URL}/currency_prices")
#     data = response.json()
    
#     # Render the data in the template
#     return render_template('home.html', data=data)

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

if __name__ == '__main__':
    app.run(port=8000, debug=True)