import controlflow as cf
from my_tools import run_google_search
from my_types import EmployeeCount, DataStack, ICPScore
from my_prettify import prettify

researcher = cf.Agent(
    "Researcher",
    instructions="""
    As a specialized company research agent, your responsibilities include:
    1. Cross-reference all findings with 1-2 additional sources.
    2. Make educated guesses when reliable sources are scarce, based on available info or company category.
    3. Prioritize the most recent data in all analyses.
    4. Cite sources and dates for all key findings, ensuring traceability.
    5. Rate confidence on a 0-5 scale for each key piece of information.
    6. Provide brief explanations for each confidence rating.
    7. Balance brevity with essential details in responses.
    8. Clearly differentiate between factual data and educated guesses.
    9. Highlight significant discrepancies between sources.
    10. Adapt research approach based on company size, industry, and public/private status.
    11. Consider recent news, market trends, and industry benchmarks in your analysis.
    12. Note any potential biases or limitations in the data sources used.
    13. Always check for the availability of real-time search tools before starting your research.
    14. If real-time search tools are unavailable, clearly state this limitation and lower confidence ratings.
    15. Factor in your training data cutoff date when real-time data is unavailable.
    16. In the absence of real-time data, state that information might be outdated and provide the date of most recent reliable data.
    """,
    tools=[run_google_search],
)


@cf.flow()
def research_flow(company_name: str):
    employee_count_task = cf.Task(
        objective=f"""Research and report on {company_name}'s employee count:
        - State whether real-time search tools were available.
        - Determine current total employee count.
        - Identify the number of data professionals, if possible.
        - Provide confidence ratings (0-5) for total count and data professionals count with brief explanations.
        - Note any significant events or discrepancies.
        - Provide the date of the most recent source used.
        """,
        tools=[run_google_search],
        agents=[researcher],
        result_type=EmployeeCount,
    )

    data_stack_task = cf.Task(
        objective=f"""Research {company_name}'s data stack:
        - Focus on job descriptions as primary sources of information.
        - Identify tools used in their data infrastructure.
        - Provide confidence ratings (0-5) for each tool identified.
        - Note any emerging trends or recent changes in their tech stack.
        """,
        tools=[run_google_search],
        agents=[researcher],
        result_type=DataStack,
    )

    icp_score_task = cf.Task(
        objective=f"""Determine ICP score for {company_name}:
        - Consider employee count and number of data professionals.
        - Analyze data stack, prioritizing: python, databricks, dbt, snowflake, kubernetes, kafka, openai, aws, gcp, azure, docker.
        - Assign higher scores for combinations of these tools, especially the first few mentioned.
        - Consider the size and maturity of the data team.
        - Provide a final ICP score (0-100) and brief explanation of the scoring.
        """,
        context=dict(employee_count=employee_count_task, data_stack=data_stack_task),
        agents=[researcher],
        result_type=ICPScore,
    )

    results = [employee_count_task.run(), data_stack_task.run(), icp_score_task.run()]

    for result in results:
        print(prettify(result))


if __name__ == "__main__":
    company_name = "Blackstone"
    research_flow(company_name)
