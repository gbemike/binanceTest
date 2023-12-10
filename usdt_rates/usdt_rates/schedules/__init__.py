from dagster import (
    AssetSelection,
    ScheduleDefinition,
)

# import the asset jobs
from ..jobs import rates_update_job, ohlc_update_job, raw_rates_job

# name: custom name given to your schedule
# job: job the schedule will run
# cron_schedule: time in which the schedule will run

# raw_rates_job schedule
raw_rates_schedule = ScheduleDefinition(
    name="raw_rates_schedule",
    job=raw_rates_job,
    cron_schedule="*/15 * * * *",
)

# raw_update_job schedule
rates_update_schedule = ScheduleDefinition(
    name="rates_update_schedule",
    job=rates_update_job,
    cron_schedule="*/15 * * * *",
)

# ohlc_update_job schedule
ohlc_update_schedule = ScheduleDefinition(
    name="ohlc_update_schedule",
    job=ohlc_update_job,
    cron_schedule="0 0 * * 0-6",
)