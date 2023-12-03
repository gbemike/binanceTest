from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
)

from .assets import rates
from .jobs import rates_update_job, ohlc_update_job, raw_rates_job
from .schedules import rates_update_schedule, ohlc_update_schedule, raw_rates_schedule

rates_assets = load_assets_from_modules([rates])

all_assets = [*rates_assets]
all_jobs = [rates_update_job, ohlc_update_job, raw_rates_job]
all_schedules = [rates_update_schedule, ohlc_update_schedule, raw_rates_schedule]

defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
)
