import requests
from bs4 import BeautifulSoup
import csv
from langdetect import detect


def is_english(description):
    try:
        return detect(description) == "en"
    except:
        return False

# Send a request to the page
url = "https://explodingtopics.com/"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to store extracted topic data
    topics = []

    # Locate each topic card within the grid container
    for card in soup.select("div.tileStyle.cardHover"):
        title = card.select_one("div.tileKeyword").text.strip() if card.select_one("div.tileKeyword") else None
        volume = card.select_one("div.scoreTag--volume .scoreTagTop").text.strip() if card.select_one("div.scoreTag--volume .scoreTagTop") else None
        growth = card.select_one(".scoreTagGradient.scoreTagTop").text.strip() if card.select_one(".scoreTagGradient.scoreTagTop") else None
        description = card.select_one("div.tileDescription").text.strip() if card.select_one("div.tileDescription") else None

        if title and volume and growth and description and is_english(description):
            topics.append({
                'title': title,
                'volume': volume,
                'growth': growth,
                'description': description
            })

    # Write the topics data to a CSV file
    with open("exploding_topics.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ['title', 'volume', 'growth', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row
        writer.writerows(topics)  # Write all valid topic rows

    print("Topics saved to exploding_topics.csv")

else:
    print("Failed to retrieve the page. Status code:", response.status_code)
