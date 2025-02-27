# LoopFX - Foreign Exchange Dashboard (Demo) Project
Scenario: A client comes to you and asks you to create a dashboard to support their trading and help them form actionable insights. They primarily trade EUR/USD, GBP/USD, EUR/GBP, and USD/CAD. They sometimes trade USD/ZAR as well. They are interested in integrating relevant supporting data but do not require it right now.

## Overview
LoopFX Dashboard is a demo project designed for traders to view live currency exchange rates and perform technical analysis. FX pricing data is fetched using `yfinance` and stored in an SQLite database. The dashboard is built with the Flask web framework and styled with Bootstrap, while interactive charts are created using Plotly.

### Features:
1. **Live Currency Tracker:**  
   Displays real-time exchange rates for key currency pairs and auto-refreshes every 10 seconds, ensuring traders always have the latest data.

2. **Interactive Charts:**  
   Users can view candlestick charts for different time periods (Today, 7 days, or 30 days) and currency pairs (EUR/USD, GBP/USD, USD/CAD, USD/ZAR, EUR/GBP). The charts also incorporate technical analysis metrics like SMA, EMA, and Bollinger Bands to help spot trends and trading signals. The chart refreshers every 10 minutes.

3. **Supporting Data Tables:**  
   Data tables display the raw numerical data below the interactive charts. These tables can be toggled on or off with a button click, offering flexibility between visualizations and raw data.

4. **API Endpoints:**  
   Robust API endpoints allow users to query currency data by pair, by period, or by combining both, facilitating easy integration with other systems.

5. **Downloadable Chart:**  
   Traders can download the interactive chart with a single click, making it easy to share analysis or save snapshots of market conditions.

6. **Theme Settings:**  
   The dashboard offers customizable theme options (Light, Dark, or Auto) to ensure a comfortable viewing experience in any environment.


## Dependencies & Running
I have consolidated all the project dependencies into a single file called `requirements.txt`. We can then set up the working environment by running the command prompts in the Terminal/Command Window in two ways,
### Using Conda:
1. **Create the Environment:**
```conda create --name loopfx_env --file requirements.txt```

2. **Activate the Environment:**
```conda activate loopfx_env```

### Using Pip:
1. **Create a Virtual Environment:**
```python -m venv loopfx_env```

2. **Activate the Virtual Environment:**
- MacOS/ Linux: ```source loopfx_env/bin/activate```
- Windows: ```loopfx_env\Scripts\activate```

3. **Install Dependencies**
```pip install -r requirements.txt```

Once the environment is set up, we can run the following script to start our API endpoints to run in backend, 
```cd currency_data_API```
```python fetch_data.py``` and 
```python api.py```

and followed by the below script to make our dashboard live (frontend).
```cd LoopFxDemo```
```python app.py```

## Thought Process
1. **Live Currency Tracker:**
To ensure traders have the most up-to-date information, I built a live currency tracker that auto-refreshes every 10 seconds. This means that exchange rates for key currency pairs are continuously updated without requiring a page refresh, giving traders real-time insights.

2. **Interactive Charts:**
Recognising that visual analysis is critical in trading, I developed interactive candlestick charts. These charts allow users to select different time periods (Today, 7 days, or 30 days) and view data for various currency pairs—including EUR/USD, GBP/USD, USD/CAD, USD/ZAR, and EUR/GBP. I also incorporated technical analysis metrics such as Simple Moving Averages (SMA), Exponential Moving Averages (EMA), and Bollinger Bands so traders can quickly spot trends and potential trading signals.

3. **Supporting Data Tables:**
In addition to the interactive charts, I added data tables that display the underlying numerical data. These tables are easily toggled on or off with a button click, giving users the flexibility to view raw data or rely solely on the visual charts.

4. **API Endpoints:**
To make the data easily accessible, I designed robust API endpoints that allow querying currency data by pair, by period, or by combining both. This not only supports our frontend’s live updates and charting but also makes it easy to integrate the data with other systems if needed.

5. **Downloadable Chart:**
I included a feature that lets users download the interactive chart with a single button click. This is especially useful for traders who need to share their analysis or archive a snapshot of the market conditions.

6. **Theme Settings:**
To enhance the user experience, the dashboard offers customizable theme options (Light, Dark, or Auto). This ensures that the interface is comfortable and accessible in any environment, whether in a bright office or a dim trading room.


## Deployment
For a project of this scale and importance, I would lean towards a more robust framework like Django rather than Flask. While Flask is great for small, straightforward projects, Django offers a comprehensive set of tools, built-in security features, and a more scalable architecture—qualities that are essential for a client-facing trading platform.
- **Backend:**
Containerize the Django app using Docker and deploy it on AWS Elastic Beanstalk for easy scaling and consistent environments across development, staging, and production.
- **Database:**
Use Amazon RDS with PostgreSQL. PostgreSQL is known for its performance, scalability, and reliability, while RDS handles automated backups, maintenance, and high availability.
- **Frontend:**
Host static assets (HTML, CSS, JS) on AWS S3 and serve them via CloudFront for fast, global delivery.
- **CI/CD & Monitoring:**
Set up a CI/CD pipeline with AWS CodePipeline for smooth deployments, and monitor performance using AWS CloudWatch.


## Use of AI
I used ChatGPT for brainstorming ideas and technical analysis, and GitHub Copilot helped debug issues and streamline code improvements. All AI-generated content was used solely as inspiration and was thoroughly reviewed to ensure that no raw AI code was directly implemented and that our final solution adhered strictly to industry best practices.
