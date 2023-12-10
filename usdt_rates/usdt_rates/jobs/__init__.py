from dagster import (
    define_asset_job,
    AssetSelection,
)

raw_rates = AssetSelection.keys(['raw_rates'])
usdt_rates = AssetSelection.keys(["usdt_rates"])
ohlc_rates = AssetSelection.keys(["ohlc_rates"])
slack_alert = AssetSelection.keys(["rate_change"])

raw_rates_job = define_asset_job(
    name="raw_rates_job",
    selection=raw_rates,
)

rates_update_job = define_asset_job(
    name="rates_update_job",
    selection=usdt_rates,
)

ohlc_update_job = define_asset_job(
    name="ohlc_update_job",
    selection=ohlc_rates,
)

slack_alert_job = define_asset_job(
    name="slack_alert_job",
    selection=slack_alert,
)