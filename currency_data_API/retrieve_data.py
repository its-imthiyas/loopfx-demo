from config import Config
from fetch_data import query_table


# Define your query
query = "SELECT * FROM currency_prices"

# Retrieve data
data_frame = query_table(query, Config.DB_PATH)

# Print the columns of the DataFrame for debugging
print("DataFrame columns:", data_frame.columns)

# Reset the index to make 'time' a regular column
data_frame.reset_index(inplace=True)

# Check if 'time' column exists before attempting to filter
if 'time' in data_frame.columns:
     # Display the retrieved data
     filtered_data = data_frame[(data_frame["pair"] == "EURUSD") & (data_frame["time"] == "2025-01-14 00:30:00")]
     print(filtered_data)
else:
     print("The 'time' column does not exist in the DataFrame.")

print(data_frame)
print(data_frame.describe())