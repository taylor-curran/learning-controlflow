import controlflow as cf
from my_tools import run_google_search
from my_types import TotalEmployeeCount, DataStack, ICPScore, DataProfessionalCount
from my_prettify import prettify


# zoominfo = company size, revenue, description -- how they make money, purpose, industry
# Links to articles discussing funding rounds

# SF account update script 

# SF
# Event in sales force - New Lead Created (Different types of leads depending on the source)

# 1. Research the company to determine what the email should include

# Zoominfo

# Sales Navigator in LinkedIn to find person's title, role, technical experience level
## Backup use google

# Use Bigquery to see if the domain exists in the user list
# Look up numbers of deployments and or blocks etc.

# 2. Write email to company based on linkedin

# zenfetch

# Outreach


researcher = cf.Agent(
    "Researcher",
    instructions="""
    You are a company research agent: cross-reference findings, prioritize recent data, cite sources, rate confidence levels, and differentiate between facts and guesses. Adapt your approach based on company specifics and note any biases or limitations in data sources.
    """,
    tools=[run_google_search],
)



@cf.flow()
def research_flow(company_name: str):
    total_employee_count_task = cf.Task(
        f"Find the current total employee count for {company_name}",
        agents=[researcher],
        result_type=TotalEmployeeCount,
    )

    data_professional_count_task = cf.Task(
        f"Find the current number of data professionals at {company_name}",
        agents=[researcher],
        result_type=DataProfessionalCount,
    )

    data_stack_task = cf.Task(
        f"Research the data technology stack used at {company_name}. Look for mentions of specific tools, technologies, and programming languages commonly used in their data workflows and projects.",
        agents=[researcher],
        result_type=DataStack,
        instructions="""
        Investigate the data technology stack used at the company. 
        Reference job descriptions for roles such as data scientists, 
        data engineers, analysts, quantitative researchers, and data research teams.
        """,
    )

    icp_score_task = cf.Task(
        objective=f"""Determine the Ideal Customer Profile (ICP) score for {company_name} on a scale of 0-100:
        - Consider the total number of employees, size of the data team, and the company's tech stack.
        - Higher scores should be given for larger employee counts and data teams.
        - The tech stack should be evaluated based on the presence of these tools (in order of importance):
        python, databricks, dbt, snowflake, kubernetes, kafka, openai, aws, gcp, azure, docker.
        - Combinations of these tools should result in even higher scores.
        - Provide a final ICP score (0-100) with a breakdown of contributing factors and a brief explanation of the scoring.
        """,
        context=dict(
            employee_count=total_employee_count_task,
            data_professional_count=data_professional_count_task,
            data_stack=data_stack_task,
        ),
        agents=[researcher],
        result_type=ICPScore,
    )


if __name__ == "__main__":
    company_name = "Blackstone"
    research_flow(company_name)
