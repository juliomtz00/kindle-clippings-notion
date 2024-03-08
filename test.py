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

# Send a POST request to retrieve data from the database
response = requests.post(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Extract 'Name' property from each entry and store in a list
    names = [entry['properties']['Name']['title'][0]['text']['content'] for entry in data['results']]
    print("Names from Notion:", names)
else:
    print("Failed to retrieve data from Notion:", response.text)