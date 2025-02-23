#########
# IMPORTS
#########
from pathlib import Path
import json
import yfinance as yf
import pandas as pd
import sqlite3
import mplfinance as mpf
import traceback
import requests_cache
import time


########
# CONFIG
########
ROOT_DIR = Path(__file__).resolve().parent.parent
# ROOT_DIR = Path.cwd().parent 
CONFIG_FILE = ROOT_DIR / "config.json"

def load_config(config):
    '''Loads config.json and returns a dictionary.
    
    Parameters
    ----------
    None
    
    
    Returns
    ----------
    dict: the variable:config pairs 
        
    '''
    
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)
    
config = load_config(config=CONFIG_FILE)
DB_PATH = (ROOT_DIR / config["DB_PATH"]).resolve()
DATA_FOLDER = (ROOT_DIR / config["DATA_FOLDER"]).resolve()
CURRENCY_PAIRS = config["CURRENCY_PAIRS"]


###########
# FUNCTIONS
###########
def define_table(path):
    '''Define schema for currency price db
    
    Parameters
    ----------
    path (str): the location of the database
    
    
    Returns
    ----------
    None
    '''  
    
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    create_price_table = '''
        CREATE TABLE IF NOT EXISTS currency_prices (
            time DATETIME NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            pair TEXT NOT NULL,
            PRIMARY KEY (time, pair)
        );
    '''

    cur.execute(create_price_table)
    conn.commit()
    conn.close()
    print("Database schema created")

def fetch_currency_data(cache, pairs, period, interval, time_sleep):
    '''Fetches currency pricing data from Yahoo Finance

    Parameters
    ----------
    pairs (list): the pairs to fetch in yfinance format (e.g. FX ends with "=X")
    period (str): data period to fetch (e.g., "1d", "5d").
    interval (str): the granularity to show for each period (e.g., "1h", "1d", "1m").
    
    Returns
    ----------
    pd.DataFrame: the fetched data in a df with all pairs concatenated 
    '''

    
    
    pair_data = []
    
    for pair in pairs:
        cleaned_pair = pair[:-2] # removes the =X from yfinance
        
        try:
            ticker = yf.Ticker(pair, session=cache) # caching to help with rate limiting
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                print(f"No data for {cleaned_pair}")
                continue

            df = df[["Open", "High", "Low", "Close"]].reset_index() # the other columns will be empty
            df.rename(columns={"Datetime": "time"}, inplace=True)
            df["pair"] = cleaned_pair
            pair_data.append(df)
            print(f"{cleaned_pair}: Data retrieved")
            
            time.sleep(time_sleep) # sleep to help with rate limiting
    
        except Exception as e:
            print(f"Issue fetching data: {e}")
            print(traceback.print_exc())
            
    if not pair_data:
        return None
    
    else:
        return pd.concat(pair_data, ignore_index=True) 
    
    
def add_to_currency_table(df, path):
    '''Inserts data into SQLite db
    
    Parameters
    ----------
    df (pd.DataFrame): the dataframe to be inserted
    path (str): the location of the database
    
    
    Returns
    ----------
    None
    '''
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    
    insert_prices = '''
        INSERT OR IGNORE INTO currency_prices (time, open, high, low, close, pair)
        VALUES (?, ?, ?, ?, ?, ?);
    '''
    # SQLite has issues with datetime
    df["time"] = df["time"].dt.strftime("%Y-%m-%d %H:%M:%S") 
    price_tuples = list(df.itertuples(index=False, name=None)) # need to be converted to tuples

    cur.executemany(insert_prices, price_tuples) # allows batching
    conn.commit()
    conn.close()

    print(f"{len(df)} records stored in database at {path}")

def query_table(query, path):
    '''General SQLite query for the db
    
    Parameters
    ----------
    query (str): the query to execute
    path (str): the location of the database
    
    Returns
    ----------
    pd.DataFrame: the result of the query as a df
    
    '''
    conn = sqlite3.connect(path)
    df = pd.read_sql(query, conn) 
    conn.close()
    
    # convert back to datetime
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"]) 
    df.set_index("time", inplace=True)  
    df.sort_index(inplace=True)    
                  
    return df

def example_plot(df, pair):
    """Queries currency data, plots candlestick chart, and saves as png in DATA FOLDER
    
    Parameters
    ----------
    pair (str): currency pair, for naming file
    
    Returns
    ----------
    None
    """

    if df.empty:
        print('No data to plot')
        return

    plot_path = DATA_FOLDER / f"{pair}_candle_chart.png"    
    
    # candlestick chart with moving average -- actual mav depends on interval
    # check out https://github.com/matplotlib/mplfinance#tutorials
    mpf.plot(df, type="candle", mav=(5), style="charles",
             title=f"{pair} Candlestick Example", ylabel="Price",
             savefig=plot_path)
    
    print(f"Sample chart saved to {plot_path}")
    
if __name__ == "__main__":
    
    # cache with one hour expiration --> easy to run into rate limits with yfinance
    session = requests_cache.CachedSession("yfinance_cache", expire_after=3600)
    
    # define table, fetch data, and add data to table
    define_table(DB_PATH)
    df = fetch_currency_data(cache=session, pairs=CURRENCY_PAIRS, period="1d", interval="30m", time_sleep=5)
    add_to_currency_table(df, DB_PATH)

    # example: pull one currency pair from the db and plot
    # yes, you could also just filter the df
    example_pair = CURRENCY_PAIRS[0][:-2] # removes =X from yfinance
    query = f"SELECT * FROM currency_prices WHERE pair = '{example_pair}'"
    example_pair_data = query_table(query, DB_PATH)
    example_plot(example_pair_data, example_pair) 
