# LoopFX - Foreign Exchange Dashboard (Demo) Project
Scenario: A client comes to you and asks you to create a dashboard to support their trading and help them form actionable insights. They primarily trade EUR/USD, GBP/USD, EUR/GBP, and USD/CAD. They sometimes trade USD/ZAR as well. They are interested in integrating relevant supporting data but do not require it right now.

## Overview
LoopFx Trading Platform is a Demo project where Traders can use it for technical analysis of the Foreign Exchange currencies, live currency comparison prices that refreshes every 30 seconds and the relevant data. The fx pricing data is fetched using 'yfinance' python library and stored in SQLITE database. These are then sent over the API endpoints from our backend to the 
- I fetched FX pricing data via `yfinance` and stored in a database
- I built a backend to...
- I included a technical analysis by...
- I developed a frontend using...

## Dependencies & Running
I created a requirements.txt file by running `conda list -e > requirements.txt`. Another user can create an environment from these requirements by running `conda create --name <env> --file requirements.txt` or `pip install -r requirements.txt`. 

To run the sample code, navigate to the backend folder `cd dashboard-starter/backend` and run sample.py. This will load the config file, fetch and store data, and generate one sample plot. 

## Thought Process
Examples:
- Based on the client's needs, I decided to build a dashboard incorporating the following currency pairs: EUR/USD, GBP/USD, EUR/GBP, USD/CAD, and USD/ZAR.
- I chose to provide X analysis in all five currencies to support the client's decision making about Y
- When gathering requirements, the client mentioned that they'd like a drilldown on EUR/USD because it accounts for 85% of their trades

## Deployment
If this was a project for a client, I would:
- Host the backend using...
- Deploy the frontend using...
- Use a cloud provider to...

## Use of AI
I used AI to get ideas about X, but I did not copy any code. I protected client information by...