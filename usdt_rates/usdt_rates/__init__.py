from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
    AssetSelection,
    ScheduleDefinition,
)

from .jobs import rates_update_job, ohlc_update_job
from .schedule import rates_update_schedule, ohlc_update_schedule

all_jobs = [rates_update_job, ohlc_update_job]
all_schedules = [rates_update_schedule, ohlc_update_schedule]

defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
)
