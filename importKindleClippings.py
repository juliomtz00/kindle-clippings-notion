'''
importKindleClippings.py

Script to import the clippings that were highlighted from the books
read on a Kindle by importing the generated .txt file where the text is
saved, so they can be exported to the notion database.

'''
import requests

# Notion API Key is generated inside the app in integrations
# Generate a new one for your own database
notionKey = "secret_vT3D6kW4xC0DlAkAHFkLb5UwRPJVxvRw8GlyUSJo7wh"

def connectToNotion():

    # Set up your Notion integration and obtain an API key
    NOTION_API_KEY = 'your_api_key_here'
    DATABASE_ID = 'your_database_id_here'

    # URL for retrieving data from the database
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

    # Headers with API key
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
    }

    # Send a GET request to retrieve data from the database
    response = requests.post(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Print retrieved data
        print(data)
    else:
        print("Failed to retrieve data from Notion:", response.text)

def main():
    try:
        # Open the file in read mode
        with open('My Clippings.txt', 'r') as file:
            # Read the file line by line
            for line in file:
                # Print each line
                print(line.strip())  # strip() removes the newline character at the end of each line
    except:
        print("Failed to open text file, please check file.")

if __name__ == "__main__":
    main()