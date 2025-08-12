
import requests
from listing import insert_or_update_listing, is_url_not_in_listings
from bs4 import BeautifulSoup
from settings import BASE_URL, HEADERS
from category import get_category_id_by_url, get_categories_urls
import re

new_listings = []

def parse_listings(category_url):
    response = requests.get(category_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    listing_grid = soup.find("div", attrs = {"data-testid" :"listing-grid"})
    cards = listing_grid.find_all('div', attrs = {"data-testid" :"l-card"})
    print(len(cards))
    for card in cards:
        tag = card.find('div', attrs = {"data-cy" :"ad-card-title"})
        if tag:
            title = tag.find('h4').text.strip()
            path = tag.find('a').get('href')
            url = BASE_URL + path
            price = tag.find('p', attrs = {"data-testid" :"ad-price"}).text.strip()
            category_id = get_category_id_by_url(category_url)
            location_date_tag = card.find('p', attrs={"data-testid": "location-date"})
            location = re.sub(r"\s*-\s*.*$", "", location_date_tag.text.strip())
            print(location)
            if is_url_not_in_listings(url):
                new_listings.append({"title": title, "path": path, "url": url, "price": price, "category": category_id})






# def parse_new_listing(listing):
#     listing_url = listing['url']
#     listing_title = listing['title']
#     listing_price = listing['price']
#     listing_category = listing['category']
#     listing_path = listing['path']
#     response = requests.get(listing_url, headers=HEADERS)
#     soup = BeautifulSoup(response.text, 'lxml')
#     description_container = soup.find('div', attrs = {"data-cy" :"ad-description"})
#     listing_description = description_container.find('div').text.strip()
#     listing_views = soup.find('span', attrs = {"data-testid" :"page-view-counter"}).text.strip()
#     parameters_container = soup.find('div', attrs = {"data-cy" :"ad-parameters-container"})
#     listing_parameters = []
#     for parameter in parameters_container.find_all('p'):
#         listing_parameters.append(parameter.text.strip())
#     image_container = soup.find('div', attrs = {"data-testid" :"image-galery-container"})
#     listing_photo_urls = []
#     for image in image_container.find_all('src'):
#         listing_photo_urls.append(image.get('src'))
#     #Parsing all listing info
#     new_listing = {"title": listing_title, "price": listing_price, "category": listing_category, "path": listing_path,
#                    "url": listing_url, "description": listing_description, "views": listing_views, "parameters": listing_parameters,
#                    "photos": listing_photo_urls, "district_id": listing_distrcit_id, "city_id": listing_city_id, "state_id": listing_state_id
#                    }
#     return new_listing




def parse_new_listing(listing_url):
    response = requests.get(listing_url, headers=HEADERS)
    print("ad-parameters-container" in response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    description_container = soup.find('div', attrs = {"data-cy" :"ad_description"})
    listing_description = description_container.find('div').text.strip()
    parameters_container = soup.find(attrs = {"data-testid":"ad-parameters-container"})
    listing_parameters = []
    for parameter in parameters_container.find_all('p'):
        listing_parameters.append(parameter.text.strip())
    image_container = soup.find('div', attrs = {"data-testid" :"image-galery-container"})
    listing_photo_urls = []
    for image in image_container.find_all('img'):
        listing_photo_urls.append(image.get('src'))
    map_section = soup.find('div', attrs = {"data-testid":"map-aside-section"})
    location_div = map_section.find_all('div')
    # location from main page
    print(location_div)
    #Parsing all listing info
    # new_listing = {
    #                "url": listing_url, "description": listing_description, "parameters": listing_parameters,
    #                "photos": listing_photo_urls[:-1], "district_id": listing_distrcit_id, "city_id": listing_city_id,
    #                 "state_id": listing_state_id
    #                }
    # print(new_listing)
# parse_new_listing("https://www.olx.ua/d/uk/obyavlenie/prodam-gazel-3302-IDYu3ew.html")


# while True:
#
#     category_urls = get_categories_urls()
#
#     for category_url in category_urls:
#         parse_listings(category_url)
#
#     for listing in new_listings:
#         new_listing = parse_new_listing(listing)
#         print(new_listing)
#         # insert_or_update_listing()


parse_listings("https://www.olx.ua/uk/transport/legkovye-avtomobili/")
