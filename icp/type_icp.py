import controlflow as cf

# ------------------------------------------------------------------------------

# create an agent to be the researcher
researcher = cf.Agent(
    "Researcher",
    instructions=f"""
    As a specialized company research agent, your responsibilities include:
    1. Cross-reference all findings with 1-2 additional sources.
    2. Make educated guesses when reliable sources are scarce, based on available info or company category.
    3. Prioritize the most recent data in all analyses.
    4. Cite sources and dates for all key findings, ensuring traceability.
    5. Rate confidence on a 0-5 scale:
       5: Multiple corroborating sources with near-identical information
       4: Strong agreement among sources with minor variations
       3: Moderate confidence, some conflicting information
       2: Low confidence, significant data gaps or conflicts
       1: Very low confidence, mostly educated guesses
       0: Complete uncertainty, speculation based on tangential information
    6. Balance brevity with essential details in responses.
    7. Flag tasks as potentially incomplete if real-time research tools are unavailable.
    8. Clearly differentiate between factual data and educated guesses.
    9. Provide brief rationales for confidence ratings.
    10. Highlight significant discrepancies between sources.
    11. Adapt research approach based on company size, industry, and public/private status.
    12. Consider recent news, market trends, and industry benchmarks in your analysis.
    13. Note any potential biases or limitations in the data sources used.
    """,
)


@cf.flow
def generate_icp_report_prompt(customer: str):
    # Task 1: Find the company's n employees
    number_of_employees = cf.Task(
        """
    Research and report on the company's employee count:
    - Determine current total employee count (or estimate a range)
    - If possible, identify the number of data professionals
    - Note significant discrepancies between sources
    - Assess recent growth trajectory
    - Compare to industry averages or key competitors

    Consider recent events (mergers, restructuring) that might affect these numbers.
    If real-time research is impossible, provide industry-standard estimates and state this limitation.
    """,
        agents=[researcher],
        instructions="""Fail this task if unable to access real-time data, but provide relevant general knowledge about the company type or industry standards.""",
    )


if __name__ == "__main__":
    generate_icp_report_prompt("Blackstone")
