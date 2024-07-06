import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")


def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_cse_id}&q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Test the Google Search function
def test_google_search():
    result = google_search("Blackstone employee count")
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Error fetching data from Google Search API")


if __name__ == "__main__":
    test_google_search()
