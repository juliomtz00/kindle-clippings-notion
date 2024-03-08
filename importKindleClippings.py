'''
importKindleClippings.py

Script to import the clippings that were highlighted from the books
read on a Kindle by importing the generated .txt file where the text is
saved, so they can be exported to the notion database.

'''
import requests

# Notion API Key is generated inside the app in integrations
# Generate a new one for your own database

def connectToNotion():

    # Set up your Notion integration and obtain an API key
    NOTION_API_KEY = "secret_vT3D6kW4xC0DlAkAHFkLb5UwRPJVxvRw8GlyUSJo7wh"
    DATABASE_ID = 'juliomr/01235d38b8eb442db43268ae198859f5?v=57479d41b04f437dafa61993b00ba8e4&pvs=4'

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
    bookTitle, bookAuthor, bookLoc, bookQuote = "", "", "", ""
    oldTitle, oldAuthor, oldLoc, oldQuote = "", "", "", ""
    newLine, saveParagraph = False, False
    try:
        # Open the file in read mode
        with open('My Clippings.txt', 'r') as file:
            i = 0
            # Read the file line by line
            for line in file:
                line.strip() # strip() removes the newline character at the end of each line

                # get book title and book author only if it is the first line or is a new line inside the file
                if i == 0 or newLine:
                    index, endIndex, newLine = line.rfind("("), line.rfind(")"), False
                    bookTitle = line[:index-1]
                    bookAuthor = line[index+1:endIndex]
                    if bookAuthor.find(",") != -1:
                        comma = bookAuthor.find(",")
                        bookAuthor = f"{bookAuthor[comma+2:]} {bookAuthor[:comma]}".strip()
                    
                
                # get the location by finding the word inside the file.
                if line.find("Location") != -1:
                    index = line.find("Location")+len("Location")+1
                    endIndex = line.find(" ",index)
                    bookLoc = line[index:endIndex]
                
                # get the quote from the file and save it
                if saveParagraph:
                    bookQuote = line.strip()
                    saveParagraph = False

                # check if the indentation indicates that it is a new line.
                if line.startswith("=========="):
                    newLine = True
                    
                    # check if there are duplicates of the highlights before saving
                    if (bookTitle == oldTitle and bookLoc == oldLoc) or i == 0:
                        oldTitle, oldAuthor, oldLoc, oldQuote = bookTitle, bookAuthor, bookLoc, bookQuote
                    else:
                        print(oldTitle, oldAuthor, oldLoc, oldQuote)
                
                # check if the quote is next as it is preceded by a blank line
                if not line.strip():
                    saveParagraph = True
                
                i+=1

    except:
        print("Failed to open text file, please check file.")   

if __name__ == "__main__":
    main()