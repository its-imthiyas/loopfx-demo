from fetch_data import query_table, DB_PATH

# Define your query
query = "SELECT * FROM currency_prices"

# Retrieve data
data_frame = query_table(query, DB_PATH)

# Display the retrieved data
print(data_frame)
