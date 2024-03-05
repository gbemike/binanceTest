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
The API is the initial point of the workspace, it provides the USDT_NGN prices we need. API reference -> https://docs.binance.us/#price-data


## Assets
* ## rates.py: 
    * raw_rates(): Retrieves the latest price information for the specified currency pairs from the Binance API and writes it to the json file raw_rates.json. raw_rates() is run every minutes.
    * usdt_rates(): This asset is a downstream data dependent on raw_rates, it reads the raw_rates.json file produced by the raw_rates asset, the function transforms the json file to a dataframe. The output of this asset is a csv file called usdt_prices. This asset is run every 15 minutes.
    * ohlc_rates(): The usdt_prices csv file is read in this asset, this asset produces ohlc values and price change for each entry in th usdt_prices csv file.

* ## alert.py:
    * rate_change():This asset is reponsible for sending slack messages to the #rate_update channel when the price change reaches a particular threshold.

## Dashboard
* streamlit_app.py: The USDT_NGN Rates Tracker is a Streamlit web application designed to visualize and analyze USDT_NGN rates over a specified date range. The app uses Plotly for interactive candlestick charting and offers a date range selection through Streamlit's user-friendly interface.
