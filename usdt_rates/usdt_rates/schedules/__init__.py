from dagster import (
    AssetSelection,
    ScheduleDefinition,
)

from ..jobs import rates_update_job, ohlc_update_job

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