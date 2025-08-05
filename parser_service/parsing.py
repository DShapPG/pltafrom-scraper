import requests
from bs4 import BeautifulSoup, NavigableString
from settings import EXCLUDED_CATEGORIES, BASE_URL, HEADERS
from category import insert_or_update_category, delete_category, get_category_id_by_slug



def parse_base_category(base_url, headers):
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    container = soup.find("div", attrs = {"data-testid":"home-categories-menu-row"})
    cards = container.find_all('a')
    print(len(cards))
    for card in cards:
        title_tag = card.find('p')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = None
        path = card.get('href')
        slug = card.get('data-path')
        category_url = base_url + path
        # print(f"Title:{title_text} Path: {slug} URL: {category_url}")
        if title and slug and category_url and path and title not in EXCLUDED_CATEGORIES:
            # print(f"Title:{type(title)} Path: {type(slug)} URL: {type(category_url)} PATH: {type(path)}")
            insert_or_update_category(title, slug, category_url, path)
            parent_id = get_category_id_by_slug(slug)
            parse_subcategory(path, parent_id)



def parse_subcategory(parent_path, parent_id):
    response = requests.get(BASE_URL + parent_path, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    links_container = soup.find("ul", attrs = {"data-testid":"category-count-links"})
    if links_container:
        cards = links_container.find_all('li')
        print(len(cards))
        for card in cards:
            tag = card.find('a')
            if tag:
                title = ''.join(t for t in tag.children if isinstance(t, NavigableString)).strip()
            else:
                title = None
            path = tag.get('href')
            slug = path.strip('/').split('/')[-1]
            if path:
                category_url = BASE_URL + path
                print(f"Title:{title} Slug: {slug} URL: {category_url} PATH: {path} Parent_id: {parent_id}")

                insert_or_update_category(title, slug, category_url, path, parent_id=parent_id)

def parse_listings(category_url):
    response = requests.get(category_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    listing_grid = soup.find("div", attrs = {"data-testid":"listing-grid"})
    cards = listing_grid.find_all('div', attrs = {"data-testid":"l-card"})
    print(len(cards))
    for card in cards:
        tag = card.find('div', attrs = {"data-cy":"ad-card-title"})
        if tag:
            title = tag.find('h4').text.strip()
            path = tag.find('a').get('href')
            print(title)


            
parse_listings("https://www.olx.ua/uk/transport/legkovye-avtomobili/")
# parse_base_category(BASE_URL, HEADERS)
