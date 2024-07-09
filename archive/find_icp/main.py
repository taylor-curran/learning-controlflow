import controlflow as cf
from my_tools import google_search_tool
from archive.find_icp.my_types import EmployeeCount
from my_prettify import prettify


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
        result_type=EmployeeCount,
    )  # TODO: I want to log how many times to search tool was used

    result = research_task.run()
    print(prettify(result))


if __name__ == "__main__":
    company_name = "Blackstone"  # You can change this to any company name
    research_flow(company_name)
