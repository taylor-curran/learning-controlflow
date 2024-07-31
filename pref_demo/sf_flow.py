from prefect import task, flow
from datetime import date, timedelta
import pandas as pd
from io import StringIO
from pydantic import BaseModel
from prefect.tasks import task_input_hash, exponential_backoff
import time
import random


class SalesforceLead(BaseModel):
    name: str
    title: str
    company: str
    email: str
    phone: str
    lead_status: str
    lead_owner: str
    industry: str
    annual_revenue: int


@task(retries=3, retry_delay_seconds=exponential_backoff(backoff_factor=2))
def fetch_salesforce_data():
    # Simulated hardcoded Salesforce data
    data = """
    Lead,Title,Company,Email,Phone,Lead Status,Lead Owner,Industry,Annual Revenue
    John Doe,Lead Software Developer,TechCorp,john.doe@techcorp.com,,Nurture,Shane Nordstrand,oil & energy,5000000
    Jane Smith,Software Engineer,InnoTech,jane.smith@innotech.com,555-1234,Nurture,Shane Nordstrand,software,12000000
    """
    time.sleep(random.uniform(1, 3))
    return data


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=30))
def convert_csv_to_df(csv_data):
    df = pd.read_csv(StringIO(csv_data))
    time.sleep(random.uniform(2, 4))
    return df


@task
def analyze_data(df):
    # Simple analysis: Count the number of leads by industry
    industry_counts = df["Industry"].value_counts()
    time.sleep(random.uniform(1, 2))
    return industry_counts


@task
def enrich_data(df):
    # Enrich data with a new column 'Lead Quality' based on 'Annual Revenue'
    df["Lead Quality"] = df["Annual Revenue"].apply(
        lambda x: "High" if x > 10000000 else "Medium"
    )
    time.sleep(random.uniform(3, 5))
    return df


@task
def save_to_database(df):
    # Simulate saving the DataFrame to a database
    print("Saving DataFrame to database...")
    time.sleep(random.uniform(2, 3))
    return "Data saved successfully"


@flow()
def salesforce_data_pipeline():
    raw_data = fetch_salesforce_data()
    df = convert_csv_to_df(raw_data)
    enriched_df = enrich_data.submit(df)
    analysis_result = analyze_data(enriched_df)

    print(f"Analysis Result:\n{analysis_result}")

    save_result = save_to_database(enriched_df)

    return save_result


if __name__ == "__main__":
    salesforce_data_pipeline()
