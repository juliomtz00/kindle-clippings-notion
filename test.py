import requests
import json
import argparse
import textwrap
from datetime import datetime, timezone

# Parse user's argument
parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter,
                                    description=textwrap.dedent('''\
        This Python script imports the clippings that were highlighted from the books
        read on a Kindle by importing the generated .txt file where the text is
        saved, so they can be exported to the notion database.

        '''))
parser.add_argument("--notion_api_key", 
                    type=str, 
                    default='NOTION_API_KEY',
                    help="Notion API KEY to generated with integrations")
parser.add_argument("--database_id", 
                    type=str, 
                    default='database_id',
                    help="Notion Database ID to write")
args = parser.parse_args()

# Set up your Notion integration and obtain an API key
NOTION_API_KEY = args.notion_api_key
DATABASE_ID = args.database_id

# URL for querying data from the database
url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

# Headers with API key and content type
headers = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    # 

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

pages = get_pages()