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


# Define the Pydantic schema for the tool's arguments
class GoogleSearchArgs(BaseModel):
    query: str


# Custom Tool Class to include args_schema
class CustomTool(Tool):
    args_schema = GoogleSearchArgs

    def __init__(self, name: str, description: str, func: callable):
        super().__init__(name=name, description=description, func=func)
        self.args_schema = GoogleSearchArgs


# Create a Tool instance for the Google Search
google_search_tool = CustomTool(
    name="google_search",
    description="Search Google for recent results.",
    func=google_search.run,
)
