import controlflow as cf
from my_tools import google_search_tool
from my_types import EmployeeCount
from my_prettify import prettify


researcher = cf.Agent(
    "Researcher",
    instructions=f"""
    As a specialized company research agent, your responsibilities include:
    1. Cross-reference all findings with 1-2 additional sources.
    2. Make educated guesses when reliable sources are scarce, based on available info or company category.
    3. Prioritize the most recent data in all analyses.
    4. Cite sources and dates for all key findings, ensuring traceability.
    5. Rate confidence on a 0-5 scale for each key piece of information:
       5: Multiple corroborating sources with near-identical information
       4: Strong agreement among sources with minor variations
       3: Moderate confidence, some conflicting information
       2: Low confidence, significant data gaps or conflicts
       1: Very low confidence, mostly educated guesses
       0: Complete uncertainty, speculation based on tangential information
    6. Provide brief explanations for each confidence rating.
    7. Balance brevity with essential details in responses.
    8. Clearly differentiate between factual data and educated guesses.
    9. Highlight significant discrepancies between sources.
    10. Adapt research approach based on company size, industry, and public/private status.
    11. Consider recent news, market trends, and industry benchmarks in your analysis.
    12. Note any potential biases or limitations in the data sources used.
    13. Always check for the availability of real-time search tools before starting your research.
    14. If real-time search tools are unavailable, clearly state this limitation and significantly lower your confidence ratings.
    15. Remember that your training data has a cutoff date, and you should factor this into your confidence ratings when real-time data is unavailable.
    16. In the absence of real-time data, clearly state that your information might be outdated and provide the approximate date of your most recent reliable data.
    """,
    tools=[google_search_tool],
)


@cf.flow
def research_flow(company_name: str):
    # Simplified research task using the Google Search tool
    research_task = cf.Task(
        objective=f"""Research and report on {company_name}'s employee count:
        - State whether real-time search tools were available like Google Search.
        - Determine current total employee count.
        - Identify the number of data professionals, if possible.
        - Provide confidence ratings (0-5) for total count and data professionals count with brief explanations.
        - Note any significant events or discrepancies.
        - Provide the date of the most recent source used.
        """,
        tools=[google_search_tool],
        agents=[researcher],
        result_type=EmployeeCount,
    )  # TODO: I want to log how many times to search tool was used

    result = research_task.run()
    print(prettify(result))


if __name__ == "__main__":
    company_name = "Blackstone"  # You can change this to any company name
    research_flow(company_name)
