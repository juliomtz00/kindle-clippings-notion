import requests
import json
from datetime import datetime, timezone

# Set up your Notion integration and obtain an API key
NOTION_API_KEY = "secret_vT3D6kW4xC0DlAkAHFkLb5UwRPJVxvRw8GlyUSJo7wh"
DATABASE_ID = '01235d38b8eb442db43268ae198859f5'

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
    with open('db.json', 'w', encoding='utf8') as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

pages = get_pages()