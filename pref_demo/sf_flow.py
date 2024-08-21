import random
import time
from datetime import timedelta, datetime
from io import StringIO
from typing import List, Union

import pandas as pd
from prefect import flow, task
from prefect.tasks import exponential_backoff, task_input_hash
from pydantic import BaseModel
from snowflake_blocks import SnowflakeConnection  # Import the custom block
from artifacts import (
    create_enriched_data_artifact,
    create_analysis_artifact,
)  # Import the artifact functions
from my_classes import SalesforceLead


@task(retries=3, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def fetch_salesforce_data():
    time.sleep(random.uniform(2, 3))
    snowflake_conn = SnowflakeConnection.load("my-snowflake-conn")
    data = snowflake_conn.read_sql("SELECT * FROM salesforce.leads")
    data_restructured = """
    Lead,Title,Company,Email,Phone,Lead Status,Lead Owner,Industry,Annual Revenue
    John Doe,Lead Software Developer,TechCorp,john.doe@techcorp.com,,Nurture,Shane Nordstrand,oil & energy,5000000
    Jane Smith,Software Engineer,InnoTech,jane.smith@innotech.com,555-1234,Nurture,Shane Nordstrand,software,12000000
    """
    return data_restructured


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def convert_csv_to_df(csv_data):
    df = pd.read_csv(StringIO(csv_data))
    time.sleep(random.uniform(2, 4))
    return df


@task(retries=4)
def analyze_data(df):
    # Simple analysis: Count the number of leads by industry
    industry_counts = df["Industry"].value_counts()
    time.sleep(random.uniform(1, 2))

    # Create a Markdown artifact after data analysis
    create_analysis_artifact(industry_counts)

    return industry_counts


@task
def enrich_data(df):
    # Enrich data with a new column 'Lead Quality' based on 'Annual Revenue'
    df["Lead Quality"] = df["Annual Revenue"].apply(
        lambda x: "High" if x > 10000000 else "Medium"
    )
    time.sleep(random.uniform(3, 5))

    # Create a Markdown artifact after data enrichment
    create_enriched_data_artifact(df)

    return df


@task
def save_to_database(df):
    # Simulate saving the DataFrame to a database
    print("Saving DataFrame to database...")
    time.sleep(random.uniform(2, 3))
    return "Data saved successfully"


@flow(persist_result=True)
def salesforce_data_pipeline(
    start_date: datetime = datetime(2023, 1, 1),
    report_type: Union[str, List[str]] = ["mql", "detailed"],
):
    print(f"Flow started with start_date: {start_date} and report_type: {report_type}")
    raw_data = fetch_salesforce_data()
    df = convert_csv_to_df(raw_data)
    enriched_df = enrich_data(df)
    analysis_result = analyze_data(enriched_df)

    print(f"Analysis Result:\n{analysis_result}")

    save_result = save_to_database(enriched_df)

    return save_result


if __name__ == "__main__":
    # Run the flow with default parameters
    salesforce_data_pipeline()

    # Deploy the flow
    # salesforce_data_pipeline.deploy(
    #     name="DEV Salesforce Data Pipeline",
    #     work_pool_name="Demo-ECS",
    #     tags=["salesforce", "data-pipeline"],
    #     image="taycurran/sf-prefect-demo:latest",
    #     triggers=[],
    # )
