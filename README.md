# Exchange Rate Tracker

This project is a Dagster-based data pipeline that tracks the USDT/NGN exchange rate from the Binance API. It fetches the latest price, stores it, calculates OHLC (Open, High, Low, Close) data, and sends notifications to a Slack channel when the price change exceeds a certain threshold. The project also includes a Streamlit application for visualizing the exchange rate data.

## Features

*   **Data Fetching:** Fetches the latest USDT/NGN exchange rate from the Binance API.
*   **Data Processing:** Calculates OHLC data and price changes.
*   **Slack Notifications:** Sends alerts to a Slack channel when the price change crosses a defined threshold.
*   **Data Visualization:** Includes a Streamlit app to visualize the exchange rate data with candlestick charts.
*   **Scheduled Execution:** Uses Dagster to schedule the data pipeline to run at regular intervals.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.9+
*   pip

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/exchange_rate_tracker.git
    cd exchange_rate_tracker
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -e ".[dev]"
    ```

### Configuration

To use the Slack notification feature, you will need to configure a Slack resource in your Dagster project.

1.  **Create a Slack App:** Follow the instructions in the [Dagster documentation](https://docs.dagster.io/integrations/slack) to create a Slack app and obtain a bot token.

2.  **Set the environment variable:** Create a `.env` file in the root of the project and add the following line:

    ```
    SLACK_BOT_TOKEN=your-slack-bot-token
    ```

    Replace `your-slack-bot-token` with the token you obtained from your Slack app.

## Usage

To run the Dagster UI and view the project, use the following command:

```bash
dagster dev
```

This will start the Dagster web server, and you can access the UI at `http://localhost:3000`.

To run the Streamlit application, use the following command:

```bash
streamlit run streamlit_app.py
```

## Project Structure

```
.
├── .gitignore
├── pyproject.toml
├── README.md
├── streamlit_app.py
├── src
│   └── exchange_rate_tracker
│       ├── __init__.py
│       ├── definitions.py
│       └── defs
│           ├── __init__.py
│           ├── assets.py
│           ├── constants.py
│           └── resources.py
└── tests
    └── __init__.py
```

*   `streamlit_app.py`: The main file for the Streamlit dashboard.
*   `src/exchange_rate_tracker/definitions.py`: The main entry point for the Dagster definitions.
*   `src/exchange_rate_tracker/defs/assets.py`: Contains the core asset definitions for the data pipeline.
*   `src/exchange_rate_tracker/defs/constants.py`: Defines constants used throughout the project.
*   `src/exchange_rate_tracker/defs/resources.py`: Defines the resources used by the project, such as the Slack resource.
*   `pyproject.toml`: The project's dependency and configuration file.