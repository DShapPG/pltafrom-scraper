import requests
from bs4 import BeautifulSoup
from settings import EXCLUDED_CATEGORIES, BASE_URL, HEADERS
from main import insert_or_update_category, delete_category


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
            print(f"Title:{type(title)} Path: {type(slug)} URL: {type(category_url)} PATH: {type(path)}")
            insert_or_update_category(title, slug, category_url, path)
            

parse_base_category(BASE_URL, HEADERS)
