from flask import Flask, jsonify, request
from fetch_data import query_table, DB_PATH, CURRENCY_PAIRS
from dbExtensions import process_dataframe

app = Flask(__name__)


@app.route('/api/currency_prices/<int:limit>', methods=['GET'])
def get_currency_all(limit: int = 10):
    query = "SELECT * FROM currency_prices LIMIT {}".format(limit)
    print(query)
    result = query_table(query, DB_PATH)
    
    result_dict = process_dataframe(result)
    
    print("Dictionary to be returned as JSON:")
    print(result_dict[:5])
    
    return jsonify(result_dict)

@app.route('/api/currency_prices_by_pair/<pair>', methods=['GET'])
def get_currency_by_pair(pair: str):
    query = "SELECT * FROM currency_prices WHERE pair = '{}'".format(pair)
    print(query)
    result = query_table(query, DB_PATH)
    
    result_dict = process_dataframe(result)
    
    print(result_dict[:5])
    
    return jsonify(result_dict)

@app.route('/api/currency_prices_by_period/<period>/<interval>', methods=['GET'])
def get_currency_by_period(period: str, interval: str):
    query = "SELECT * FROM currency_prices WHERE time >= datetime('now', '-{} days".format(period)
    print(query)
    result = query_table(query, DB_PATH)
    
    result_dict = process_dataframe(result)
    
    print(result_dict[:5])
    
    return jsonify(result_dict)

if __name__ == '__main__':
   app.run(port=5000,debug=True)