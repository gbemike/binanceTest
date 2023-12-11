from dagster import (
    Definitions,
    load_assets_from_modules,
    define_asset_job,
    EnvVar
)

from dagster_slack import SlackResource

from .assets import rates, alert
from .jobs import rates_update_job, ohlc_update_job, raw_rates_job, slack_alert_job
from .schedules import rates_update_schedule, ohlc_update_schedule, raw_rates_schedule

# higher level view of our dagster task

# loads all our assets into the variables below
rates_assets = load_assets_from_modules([rates])
alert_assets = load_assets_from_modules([alert])

# list containing all assets
all_assets = [*rates_assets,*alert_assets]

# list containing all jobs
all_jobs = [rates_update_job, ohlc_update_job, raw_rates_job, slack_alert_job]

# list containing all schedules
all_schedules = [rates_update_schedule, ohlc_update_schedule, raw_rates_schedule]

# Defintions contain all the ingridients needed for our dagster task
defs = Definitions(
    assets=all_assets,
    jobs=all_jobs,
    schedules=all_schedules,
    resources={
        # define slack api token
        "slack_resource": SlackResource(token=EnvVar("MY_SLACK_TOKEN")),
    }
)
