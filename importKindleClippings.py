'''
importKindleClippings.py

Script to import the clippings that were highlighted from the books
read on a Kindle by importing the generated .txt file where the text is
saved, so they can be exported to the notion database.

'''
import requests
import argparse
import textwrap

# Notion API Key is generated inside the app in integrations
# Generate a new one for your own database

def connectToNotion(NOTION_API_KEY, DATABASE_ID):
    pass

def main():

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

    bookTitle, bookAuthor, bookLoc, bookQuote = "", "", "", ""
    oldTitle, oldAuthor, oldLoc, oldQuote = "", "", "", ""
    saveParagraph = False
    try:
        # Open the file in read mode
        with open('My Clippings.txt', 'r') as file:
            i = 0
            # Read the file line by line
            for line in file:
                # strip() removes the newline character at the end of each line

                # get book title and book author only if it is the first line or is a new line inside the file
                if line.strip().endswith(")"):
                    index = line.rfind("(")
                    bookTitle = line[:index-1]
                    bookAuthor = line[index+1:-1]
                    if bookAuthor.find(",") != -1:
                        comma = bookAuthor.find(",")
                        bookAuthor = f"{bookAuthor[comma+2:]} {bookAuthor[:comma]}".strip()
                    print(bookTitle, bookAuthor)
                    
                # get the location by finding the word inside the file.
                elif line.find("Location") != -1:
                    index = line.find("Location")+len("Location")+1
                    endIndex = line.find(" ",index)
                    bookLoc = line[index:endIndex]
                
                # get the quote from the file and save it
                elif saveParagraph:
                    bookQuote = line.strip()
                    saveParagraph = False

                # check if the quote is next as it is preceded by a blank line
                if not line.strip():
                    saveParagraph = True
    except:
        print("Failed to open text file, please check file.")   

if __name__ == "__main__":
    main()