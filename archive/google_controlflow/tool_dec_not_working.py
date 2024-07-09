from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
import controlflow as cf
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from controlflow import tool

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

# Initialize the Google Search API Wrapper
google_search = GoogleSearchAPIWrapper(
    google_api_key=google_api_key, google_cse_id=google_cse_id
)


# Define the Pydantic schema for the tool's arguments
class GoogleSearchArgs(BaseModel):
    query: str


# Define the tool using the @tool decorator
@tool(
    name="google_search",
    description="Search Google for recent results.",
    args_schema=GoogleSearchArgs,
)
def google_search_tool(query: str):
    return google_search.run(query)


# Create a research task using the Google Search tool
research_task = cf.Task(
    objective="Research how many employees are in the Blackstone company",
    tools=[google_search_tool],
)

if __name__ == "__main__":
    result = research_task.run()
    print(f"Research result: {result}")
