import pandas as pd
import sqlite3


#Defining a Table for Fx Values
def define_table(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    
    create_fxvalue_table = '''
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
    
    cursor.execute(create_fxvalue_table)
    connection.commit()
    connection.close()
    print("Table created successfully")
    

def add_to_currency_table(df, path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    
    insert_fxvalue = '''
        INSERT OR IGNORE INTO currency_prices (time, open, high, low, close, pair)
        VALUES (?, ?, ?, ?, ?, ?);
    '''
    
    df["time"] = df["time"].dt.strftime("%Y-%m-%d %H:%M:%S") 
    fxvalue_tuples = list(df.itertuples(index=False, name=None)) 
    cursor.executemany(insert_fxvalue, fxvalue_tuples)
    connection.commit()
    connection.close()
    print(f"{len(df)} records stored in database at {path}")
    
def query_table(query, path, params=()):
    connection = sqlite3.connect(path)
    df = pd.read_sql(query, connection, params=params) 
    connection.close()
    
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"]) 
    df.set_index("time", inplace=True)  
    df.sort_index(inplace=True)    
    return df