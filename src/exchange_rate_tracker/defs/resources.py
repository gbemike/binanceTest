import os

import dagster as dg
from dagster import EnvVar
from dagster_slack import SlackResource
from dotenv import load_dotenv

load_dotenv()

token = EnvVar("MY_SLACK_TOKEN")

slack_integration = SlackResource(token=token)

@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "slack_resource": slack_integration,
        }
    )