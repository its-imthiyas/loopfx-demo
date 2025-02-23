import pandas as pd

def process_dataframe(result):
    # Debug print to check the DataFrame
    print("DataFrame retrieved from database:")
    print(result.head())
    
    # Ensure the 'time' column is in the correct format
    if 'time' in result.columns:
        result['time'] = result['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Convert the DataFrame to a dictionary
    result_dict = result.reset_index().to_dict(orient='records')
    
    # Debug print to check the dictionary
    print("Dictionary to be returned as JSON:")
    print(result_dict[:5])
    
    return result_dict