import controlflow as cf
# from langchain_community.utilities import GoogleSearchAPIWrapper

# # ------------------------------------------------------------------------------

# search = GoogleSearchAPIWrapper()

# create an agent to be the researcher
researcher = cf.Agent(
    "Researcher",
    instructions=f"""
        You are a researcher of companies. When you find your answer, you always try to cross reference that information with another source or two. When you can't find a decent source for the information you research, you should make an educated guess based on the information you have found or the general category of the company. You should also make sure to note the sources of your information. You also always score your confidence in your answer from 0 to 5. A 5 means you found multiple sources with identical or very similar answers. A 0 means you had to make a wild guess.""",
    # tools=[GoogleSearchAPIWrapper()],
)


@cf.flow
def generate_icp_report(customer: str):
    number_of_employees = cf.Task(
        """
    In this task, the researcher agent will see if there is available information to find the most likely number of employees in the company currently. They will then see if there is more specific information about the number of data professionals in the company.
    """,
        agents=[researcher],
    )


if __name__ == "__main__":
    generate_icp_report("Blackstone")
