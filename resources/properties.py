import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://www.lookup.properties/vivian-karanja/#'

# Send an HTTP request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Find property listings (you'll need to inspect the page to get the correct tags)
    properties = soup.find_all('div', class_='property-item')

    # Extract information for each property
    for property in properties:
        title = property.find('h2', class_='property-title').get_text(strip=True)
        price = property.find('span', class_='property-price').get_text(strip=True)
        location = property.find('div', class_='property-location').get_text(strip=True)
        
        # Print the details of each property
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Location: {location}")
        print('-' * 40)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
