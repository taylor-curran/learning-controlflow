from dotenv import load_dotenv
import os
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
import controlflow as cf
from prettify_my_stuff import pretty_print_employee_count

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

# Ensure that environment variables are loaded correctly
if not google_api_key or not google_cse_id:
    raise ValueError(
        "Google API key and CSE ID must be set in the environment variables."
    )

# Initialize the Google Search API Wrapper
google_search = GoogleSearchAPIWrapper(
    google_api_key=google_api_key, google_cse_id=google_cse_id
)

# Verify the search instance is created correctly
if not google_search:
    raise ValueError("Failed to create GoogleSearchAPIWrapper instance.")

# Create a Tool instance for the Google Search
google_search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=google_search.run,
)

# Verify the tool is created correctly
if not google_search_tool:
    raise ValueError("Failed to create Google Search tool instance.")

# Create an agent that uses the Google Search tool
researcher = cf.Agent(
    name="Researcher",
    instructions="""
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
def generate_icp_report(customer: str):
    number_of_employees = cf.Task(
        objective=f"Research and report on {customer}'s employee count",
        instructions=f"""
        Research and report on {customer}'s employee count:
        - Determine current total employee count (or estimate a range)
        - If possible, identify the number of data professionals
        - Assess recent growth trajectory (annual growth rate)
        - Compare to industry averages
        - Provide confidence ratings (0-5) with brief explanations for total count, data professionals count, and growth rate
        - Note any significant events or discrepancies
        - Provide all available information in the required format.
        - Before starting your research, explicitly check if you have access to real-time search tools.
        - If real-time search tools are unavailable, clearly state this limitation in your report and adjust your confidence ratings accordingly.
        - Provide the approximate date of your most recent reliable data when real-time data is unavailable.
        - Remember that your training data has a cutoff date, and factor this into your confidence ratings.
        """,
        agents=[researcher],
    )

    result = number_of_employees.run()
    if result is None:
        print(f"Failed to gather information for {customer}. No data available.")
    else:
        pretty_print_employee_count(result)


if __name__ == "__main__":
    generate_icp_report("Blackstone")
