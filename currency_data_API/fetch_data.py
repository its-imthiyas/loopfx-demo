from pathlib import Path
import json
import yfinance as yf
import pandas as pd
import sqlite3
import mplfinance as mpf
import traceback
import requests_cache
import time
from config import Config
from database import define_table, add_to_currency_table, query_table


def fetch_currency_data(cache, pairs, period, interval, time_sleep):
    pair_data = []
    
    for pair in pairs:
        cleaned_pair = pair[:-2] # removes the =X from yfinance
        
        try:
            ticker = yf.Ticker(pair, session=cache) # caching to help with rate limiting
            fxdata_df = ticker.history(period=period, interval=interval)

            if fxdata_df.empty:
                print(f"No data for {cleaned_pair}")
                continue

            fxdata_df = fxdata_df[["Open", "High", "Low", "Close"]].reset_index() # the other columns will be empty
            fxdata_df.rename(columns={"Datetime": "time"}, inplace=True)
            fxdata_df["pair"] = cleaned_pair
            pair_data.append(fxdata_df)
            print(f"{cleaned_pair}: Data retrieved")
            
            time.sleep(time_sleep) # sleep to help with rate limiting
    
        except Exception as e:
            print(f"Issue fetching data: {e}")
            print(traceback.print_exc())
            
    if not pair_data:
        return None
    
    else:
        return pd.concat(pair_data, ignore_index=True) 
    
    

def example_plot(fxdata_df, pair):
    if fxdata_df.empty:
        print('No data to plot')
        return

    plot_path = Config.DATA_FOLDER / f"{pair}_candle_chart.png"    
    
    # candlestick chart with moving average -- actual mav depends on interval
    # check out https://github.com/matplotlib/mplfinance#tutorials
    mpf.plot(fxdata_df, type="candle", mav=(5), style="charles",
             title=f"{pair} Candlestick Example", ylabel="Price",
             savefig=plot_path)
    
    print(f"Sample chart saved to {plot_path}")

    
if __name__ == "__main__":
    # cache with one hour expiration --> easy to run into rate limits with yfinance
    session = requests_cache.CachedSession("yfinance_cache", expire_after=3600)
    
    # define table, fetch data, and add data to table
    define_table(Config.DB_PATH)
    fxdata_df = fetch_currency_data(cache=session, pairs=Config.CURRENCYPAIRS, period="30d", interval="30m", time_sleep=5)
    add_to_currency_table(fxdata_df, Config.DB_PATH)

    # example: pull one currency pair from the db and plot
    # yes, you could also just filter the fxdata_df
    example_pair = Config.CURRENCYPAIRS[0][:-2] # removes =X from yfinance
    query = f"SELECT * FROM currency_prices WHERE pair = '{example_pair}'"
    example_pair_data = query_table(query, Config.DB_PATH)
    example_plot(example_pair_data, example_pair) 
