from flask import Flask, jsonify, request
from fetch_data import query_table
from config import Config
from utilities import process_dataframe
import logging

app = Flask(__name__)
app.config.from_object(Config)

#Settting up Logging for the API
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#API endpoint to get all currency prices (default limit is 10 entries)
@app.route('/api/currency_prices/<int:limit>', methods=['GET'])
def get_currency_all(limit: int = 10):
    try:
        query = "SELECT * FROM currency_prices LIMIT ?"
        result = query_table(query, app.config["DB_PATH"], (limit,))
        result_dict = process_dataframe(result)
        return jsonify(result_dict)
    except Exception as e:
        logger.error(f"Error fetching currency prices: {e}")
        return jsonify({"error": "An error occurred while fetching data."}), 500
    
# Home page route that calls the same function with a default limit of 10
@app.route('/', methods=['GET'])
def home():
    return get_currency_all(10)
    
#API endpoint to get currency prices by pair (eg: EURUSD)    
@app.route('/api/currency_prices_by_pair/<pair>', methods=['GET'])
def get_currency_by_pair(pair: str):
    try:
        query = "SELECT * FROM currency_prices WHERE pair = ?"
        result = query_table(query, app.config["DB_PATH"], (pair,))
        result_dict = process_dataframe(result)
        return jsonify(result_dict)
    except Exception as e:
        logger.error(f"Error fetching currency prices: {e}")
        return jsonify({"error": "An error occurred while fetching data."}), 500

#API endpoint to get currency prices by pair and period (eg: EURUSD and 30 days)
@app.route('/api/currency_prices_by_pair_and_period/<pair>/<int:period>', methods=['GET'])
def get_currency_by_pair_and_period(pair: str, period: int):
    try:
        query = "SELECT * FROM currency_prices WHERE pair = ? AND time >= datetime('now', ?)"
        result = query_table(query, app.config['DB_PATH'], (pair, f'-{period} days'))
        result_dict = process_dataframe(result)
        return jsonify(result_dict)
    except Exception as e:
        logger.error(f"Error fetching currency prices for pair {pair} and period {period}: {e}")
        return jsonify({"error": "An error occurred while fetching data."}), 500

#API endpoint to get currency prices by period (eg: 10 days)
@app.route('/api/currency_prices_by_period/<period>', methods=['GET'])
def get_currency_by_period(period: str):
    try:
        query = "SELECT * FROM currency_prices WHERE time >= datetime('now', ?)"
        result = query_table(query, app.config['DB_PATH'], (f'-{period} days',)) 
        result_dict = process_dataframe(result)
        return jsonify(result_dict)
    except Exception as e:
        logger.error(f"Error fetching currency prices for period {period}: {e}")
        return jsonify({"error": "An error occurred while fetching data."}), 500

if __name__ == '__main__':
      # Print all configuration values
    print("App configuration:")
    for key, value in app.config.items():
        print(f"{key}: {value}")
    app.run(port=app.config['PORT'], debug=app.config['DEBUG'])