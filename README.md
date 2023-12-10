# USDT rates retrieval 
This workspacde contains scripts that retrieve the USDT_NGN rates to be schedules every 15 minutes and retrieve the
ohlc values so it can be plotted on a candlestick chart in Streamlit and show live trends and analysis

## Getting started

First, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
pip install -e ".[dev]"
```

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `usdt_rates/assets.py`. The assets are automatically loaded into the Dagster code location as you define them.

## API
The API is the initial point of the workspace, it provides the USDT_NGN prices we need.


## Assets
* app.py: Retrieves the latest price information for the specified currency pairs from the Binance API, formats the data then 
appends the data to the  initial dataframe. Subsequently, the transformed dataframe, now featuring Open-High-Low-Close (OHLC) values, is appended to a new CSV file for comprehensive and organized data storage.


* streamlit_app.py: The USDT_NGN Rates Tracker is a Streamlit web application designed to visualize and analyze USDT_NGN rates over a specified date range. The app uses Plotly for interactive candlestick charting and offers a date range selection through Streamlit's user-friendly interface.


- [ ] Orchestrate the project with Dagster to send API requests every 15 minutes
- [ ] Trigger Slack notifications (using Dagster) on significant rate change
    - [ ] Get the stakeholder requirement on significant rate change value