import pandas as pd
from config import Config
import logging
import sqlite3

#Setting up Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_dataframe(result):
    try:
        # Debugging log to check the DataFrame
        logger.debug("DataFrame retrieved from database:")
        logger.debug(result.head())
    
        # Ensuring the 'time' column is in the correct format
        if 'time' in result.columns:
            result['time'] = result['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
        # Converting the DataFrame to a dictionary
        result_dict = result.reset_index().to_dict(orient='records')
    
        # Debug log to check the dictionary
        logger.debug("Dictionary to be returned as JSON:")
        logger.debug(result_dict[:5])
    
        return result_dict
    except Exception as e:
        logger.error(f"Error processing DataFrame: {e}")
        raise
