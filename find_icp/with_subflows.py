import controlflow as cf
from my_tools import run_google_search
from my_types import TotalEmployeeCount, DataStack, ICPScore, DataProfessionalCount
from my_prettify import prettify

researcher = cf.Agent(
    "Researcher",
    instructions="""
    You are a company research agent: cross-reference findings, prioritize recent data, cite sources, rate confidence levels, and differentiate between facts and guesses. Adapt your approach based on company specifics and note any biases or limitations in data sources.
    """,
    tools=[run_google_search],
)


@cf.flow()
def get_total_employee_count(company_name: str) -> TotalEmployeeCount:
    return cf.Task(
        f"Find the current total employee count for {company_name}",
        agents=[researcher],
        result_type=TotalEmployeeCount,
    )


@cf.flow()
def get_data_professional_count(company_name: str) -> DataProfessionalCount:
    return cf.Task(
        f"Find the current number of data professionals at {company_name}",
        agents=[researcher],
        result_type=DataProfessionalCount,
    )


@cf.flow()
def get_data_stack(company_name: str) -> DataStack:
    return cf.Task(
        f"Research the data technology stack used at {company_name}. Look for mentions of specific tools, technologies, and programming languages commonly used in their data workflows and projects.",
        agents=[researcher],
        result_type=DataStack,
        instructions="""
        Investigate the data technology stack used at the company. 
        Reference job descriptions for roles such as data scientists, 
        data engineers, analysts, quantitative researchers, and data research teams.
        """,
    )


@cf.flow()
def calculate_icp_score(
    company_name: str,
    employee_count: TotalEmployeeCount,
    data_professional_count: DataProfessionalCount,
    data_stack: DataStack,
) -> ICPScore:
    return cf.Task(
        objective=f"""Determine the Ideal Customer Profile (ICP) score for {company_name} on a scale of 0-100:
        - Consider the total number of employees, size of the data team, and the company's tech stack.
        - Higher scores should be given for larger employee counts and data teams.
        - The tech stack should be evaluated based on the presence of these tools (in order of importance):
        python, databricks, dbt, snowflake, kubernetes, kafka, openai, aws, gcp, azure, docker.
        - Combinations of these tools should result in even higher scores.
        - Provide a final ICP score (0-100) with a breakdown of contributing factors and a brief explanation of the scoring.
        """,
        context=dict(
            employee_count=employee_count,
            data_professional_count=data_professional_count,
            data_stack=data_stack,
        ),
        agents=[researcher],
        result_type=ICPScore,
    )


@cf.flow()
def research_flow_parent(company_name: str):
    total_employee_count = get_total_employee_count(company_name)
    data_professional_count = get_data_professional_count(company_name)
    data_stack = get_data_stack(company_name)
    icp_score = calculate_icp_score(
        company_name, total_employee_count, data_professional_count, data_stack
    )
    return icp_score


if __name__ == "__main__":
    company_name = "Fidelity Investments"
    research_flow_parent(company_name)
