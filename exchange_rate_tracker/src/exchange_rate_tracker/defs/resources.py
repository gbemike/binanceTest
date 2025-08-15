import os
import dagster as dg
from dagster import EnvVar
from dagster_slack import SlackResource
from dotenv import load_dotenv

load_dotenv()

slack_resource = SlackResource(token=os.getenv("MY_SLACK_TOKEN"))

@dg.definitions
def resources():
    return dg.Definitions(
        resources={
            "slack_resource": slack_resource,
        }
    )