# artifacts.py
from prefect.artifacts import create_markdown_artifact


def create_enriched_data_artifact(df):
    enriched_markdown_report = f"""# Enriched Data Report

## Summary

Data has been enriched with the 'Lead Quality' column.

## Enriched Data (sample)

{df.head().to_markdown(index=False)}
"""
    create_markdown_artifact(
        key="enriched-data-report",
        markdown=enriched_markdown_report,
        description="Report after enriching data with Lead Quality column.",
    )


def create_analysis_artifact(analysis_result):
    analysis_markdown_report = f"""# Analysis Report

## Summary

Analysis of leads by industry.

## Industry Counts

{analysis_result.to_markdown()}
"""
    create_markdown_artifact(
        key="analysis-report",
        markdown=analysis_markdown_report,
        description="Report after analyzing leads by industry.",
    )
