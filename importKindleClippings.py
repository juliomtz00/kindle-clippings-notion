import os
import json
import requests
from dotenv import load_dotenv
import platform

# Load environment variables
load_dotenv()

# Notion API Details
NOTION_API_URL = "https://api.notion.com/v1/pages"

# File paths
CLIPPINGS_FILE_NAME = "My Clippings.txt"
SAVED_CLIPPINGS_DB = "oldQuotes.json"


def find_kindle_device():
    """ Find the mounted path of the Kindle device. """
    kindle_path = "/Volumes/Kindle/documents"

    if kindle_path:
        # Check if My Clippings.txt exists in the expected directory
        clippings_file_path = os.path.join(kindle_path, CLIPPINGS_FILE_NAME)
        if os.path.exists(clippings_file_path):
            return clippings_file_path

    return None


def load_existing_clippings():
    """ Load previously saved clippings from JSON. """
    if os.path.exists(SAVED_CLIPPINGS_DB):
        try:
            with open(SAVED_CLIPPINGS_DB, "r", encoding="utf-8") as file:
                return json.load(file) or []
        except json.JSONDecodeError:
            print("Warning: previousClippings.json is invalid. Resetting.")
            return []
    return []


def save_new_clippings(new_clippings):
    """ Save new clippings to JSON. """
    existing_clippings = load_existing_clippings()
    existing_set = {(clip["book_title"], clip["highlight"]) for clip in existing_clippings}

    # Compare and keep only the longest highlight
    for new_clip in new_clippings:
        book_title = new_clip["book_title"]
        new_quote = new_clip["highlight"]
        longest_quote = None

        # Check if the new quote is a longer version of an existing one
        for existing_clip in existing_clippings:
            existing_quote = existing_clip["highlight"]
            if new_quote in existing_quote or existing_quote in new_quote:
                longest_quote = max(existing_quote, new_quote, key=len)
                break

        # If no similar quote exists, just add it to the list
        if not longest_quote:
            longest_quote = new_quote

        # Add the longest quote to the set and update the list
        if (book_title, longest_quote) not in existing_set:
            existing_set.add((book_title, longest_quote))
            existing_clippings.append({
                "book_title": book_title,
                "book_author": new_clip["book_author"],
                "book_location": new_clip["book_location"],
                "highlight": longest_quote
            })

    # Save the updated list of clippings
    with open(SAVED_CLIPPINGS_DB, "w", encoding="utf-8") as file:
        json.dump(existing_clippings, file, indent=4)


def parse_clippings_file():
    """ Extract book highlights from 'My Clippings.txt'. """
    new_clippings = []
    existing_clippings = load_existing_clippings()
    existing_set = {(clip["book_title"], clip["highlight"]) for clip in existing_clippings}

    # Find Kindle device and open clippings file
    kindle_file_path = find_kindle_device()

    if not kindle_file_path:
        print("Error: Kindle not found or 'My Clippings.txt' not found.")
        return []

    book_title, book_author, book_location, book_quote = "", "", "", ""
    save_next_line = False

    try:
        with open(kindle_file_path, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Book Title & Author
                if line.endswith(")"):
                    index = line.rfind("(")
                    book_title = line[:index - 1].strip()
                    book_author = line[index + 1:-1].strip()

                # Location
                elif "Location" in line:
                    index = line.find("Location") + len("Location") + 1
                    end_index = line.find(" ", index)
                    book_location = line[index:end_index].strip() if end_index != -1 else line[index:].strip()

                # Highlighted Text
                elif save_next_line:
                    book_quote = line
                    save_next_line = False

                    # Avoid duplicates
                    if book_title and book_quote and (book_title, book_quote) not in existing_set:
                        new_clippings.append({
                            "book_title": book_title,
                            "book_author": book_author,
                            "book_location": book_location,
                            "highlight": book_quote
                        })
                        existing_set.add((book_title, book_quote))

                # Blank line means next line is a highlight
                if line == "":
                    save_next_line = True

    except FileNotFoundError:
        print(f"Error: {kindle_file_path} not found.")

    return new_clippings


def add_highlight_to_notion(NOTION_DATABASE_ID, NOTION_TOKEN, book_title, highlight):
    """ Upload a highlight to Notion. """

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Prepare the data
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": highlight}}]
            },
            "Book Name Text": {
                "rich_text": [{"text": {"content": book_title}}]
            },
            "Notebook": {
                "relation": [{"id": "11971232b71b80978d15d5c9b9a5e048"}]  # Assuming this is the fixed Notebook ID
            }
        }
    }

    response = requests.post(NOTION_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"✅ Added highlight from '{book_title}': {highlight}")
    else:
        print(f"❌ Failed to add highlight: {response.status_code}, {response.text}")


def sync_clippings():
    """ Main function to parse, filter, save, and upload highlights. """
    load_dotenv(dotenv_path='credentials.env')
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")

    print("📖 Reading clippings from Kindle...")
    new_highlights = parse_clippings_file()

    if not new_highlights:
        print("✅ No new highlights found.")
        return

    print("💾 Saving new highlights locally...")
    save_new_clippings(new_highlights)

    print("📤 Uploading new highlights to Notion...")
    for entry in new_highlights:
        print(f"📚 Book: {entry['book_title']}, Highlight: {entry['highlight']}")
        add_highlight_to_notion(NOTION_DATABASE_ID, NOTION_TOKEN, entry["book_title"], entry["highlight"])

    print("🎉 Sync complete!")


if __name__ == "__main__":
    sync_clippings()
