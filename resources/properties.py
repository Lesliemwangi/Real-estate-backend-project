import requests
from bs4 import BeautifulSoup
import time

# Base URL of the website to scrape
base_url = 'https://www.lookup.properties/'

def scrape_properties():
    # Send an HTTP request to the website
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"HTTP request failed: {e}")
        return None

    # List to store property links by county
    county_links = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the "Properties By County" menu
        properties_by_county = soup.find('li', id='menu-item-6624')
        if properties_by_county:
            sub_menu = properties_by_county.find('ul', class_='sub-menu')
            if sub_menu:
                # Extract links for each county
                for item in sub_menu.find_all('li'):
                    link = item.find('a')
                    if link and 'href' in link.attrs:
                        county_name = link.get_text(strip=True)
                        county_url = link['href']
                        # Scrape properties for each county
                        properties = scrape_county_properties(county_url)
                        county_links.append({
                            'county': county_name,
                            'url': county_url,
                            'properties': properties
                        })
                    time.sleep(2)  # Delay between county requests to avoid overwhelming the server
            else:
                print("No sub-menu found for Properties By County.")
                return None
        else:
            print("Properties By County menu item not found.")
            return None
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    return county_links

def scrape_county_properties(county_url):
    # Define headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.lookup.properties/'
    }
    
    # Send an HTTP request to the county properties page with headers
    try:
        response = requests.get(county_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"HTTP request for county properties failed: {e}")
        return []

    properties = []
    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming property details are within a specific HTML structure
    # You might need to adjust the selectors based on the actual structure
    property_cards = soup.find_all('div', class_='property-card')  # Example class name

    for card in property_cards:
        title = card.find('h2', class_='property-title').get_text(strip=True)  # Adjust selectors
        price = card.find('span', class_='property-price').get_text(strip=True)  # Adjust selectors
        link = card.find('a', class_='property-link')['href']  # Adjust selectors

        properties.append({
            'title': title,
            'price': price,
            'url': link
        })

    return properties

# Entry point: this will run when the script is called directly
if __name__ == "__main__":
    properties = scrape_properties()
    if properties:
        for county in properties:
            print(f"County: {county['county']}")
            print(f"URL: {county['url']}")
            for prop in county['properties']:
                print(f"  Title: {prop['title']}")
                print(f"  Price: {prop['price']}")
                print(f"  Link: {prop['url']}")
            print('-' * 40)
    else:
        print("Failed to retrieve property data")
