from dagster import (
    load_assets_from_modules,
    define_asset_job,
    AssetSelection,
)

from . import assets

all_assets = load_assets_from_modules([assets])

usdt_rates = AssetSelection.keys(["usdt_rates"])
ohlc_rates = AssetSelection.keys(["ohlc_rates"])

rates_update_job = define_asset_job(
    name="rates_update_job",
    selection=usdt_rates,
)

ohlc_update_job = define_asset_job(
    name="ohlc_update_job",
    selection=ohlc_rates,
)
