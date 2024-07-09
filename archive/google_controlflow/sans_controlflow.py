from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
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


# Example function to use the Google Search tool directly
def run_google_search(query):
    result = google_search_tool.run(query)
    print(f"Search result for '{query}': {result}")


if __name__ == "__main__":
    run_google_search("Find Blackstone employee count")
