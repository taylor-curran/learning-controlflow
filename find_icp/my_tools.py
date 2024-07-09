from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from pydantic import BaseModel
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


def run_google_search(query: str) -> str:
    """Search Google for recent results."""
    return google_search.run(query=query)
