from dagster import (
    define_asset_job,
    AssetSelection,
)

# AsserSelection Returns a selection that includes assets with any of the 
# provided keys and all asset checks that target them

raw_rates = AssetSelection.keys(['raw_rates'])
usdt_rates = AssetSelection.keys(["usdt_rates"])
ohlc_rates = AssetSelection.keys(["ohlc_rates"])
slack_alert = AssetSelection.keys(["rate_change"])

# define_asset_job() defines a dagster job
# selection signifies what asset should is being defined it the job

# raw_rates asset job
raw_rates_job = define_asset_job(
    name="raw_rates_job",
    selection=raw_rates,
)

# usdt_rates asset job
rates_update_job = define_asset_job(
    name="rates_update_job",
    selection=usdt_rates,
)
# ohlc_rates asset job
ohlc_update_job = define_asset_job(
    name="ohlc_update_job",
    selection=ohlc_rates,
)

# slack_alert asset job
slack_alert_job = define_asset_job(
    name="slack_alert_job",
    selection=slack_alert,
)