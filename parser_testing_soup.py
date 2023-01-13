from bs4 import BeautifulSoup
import requests

# Send a request to the website
response = requests.get('http')

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the chapters on the page
chapters = soup.find_all('li', class_='wp-manga-chapter')

# Create a dictionary to store the chapters and their corresponding image lists
for chapter in chapters:
    chapter_link = chapter.find('a').get('href')
    print(chapter_link)

# Iterate through the chapters and scrape the images
for chapter in chapters:
    # Send a request to the chapter URL
    response = requests.get(chapter)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the images on the page
    images = soup.find_all('img', class_='wp-manga-chapter-img')

    # Add the images to the dictionary
    for image in images:
        print(image.get('data-src'))      
