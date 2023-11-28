from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
    AssetSelection,
    ScheduleDefinition,
)

from dagster_slack import SlackResource

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

rates_update_schedule = ScheduleDefinition(
    name="rates_update_schedule",
    job=rates_update_job,
    cron_schedule="*/15 * * * *",
)

ohlc_update_schedule = ScheduleDefinition(
    name="ohlc_update_schedule",
    job=ohlc_update_job,
    cron_schedule="0 0 * * 0-6",
)

all_jobs = [rates_update_job, ohlc_update_job]
all_schedules = [rates_update_schedule, ohlc_update_schedule]

defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
)
