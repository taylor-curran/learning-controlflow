from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
import controlflow as cf
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

# Initialize the Google Search API Wrapper
google_search = GoogleSearchAPIWrapper(
    google_api_key=google_api_key, google_cse_id=google_cse_id
)

# Create a Tool instance for the Google Search
google_search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=google_search.run,
)

# Create a research task using the Google Search tool
research_task = cf.Task(
    "Research how many employees are in the Blackstone company",
    tools=[google_search_tool],
)

if __name__ == "__main__":
    result = research_task.run()
    print(f"Research result: {result}")
