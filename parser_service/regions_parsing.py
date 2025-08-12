import requests
from region import insert_or_update_region
from settings import BASE_URL, HEADERS


def parse_regions():
    regions_api = "https://www.olx.ua/api/v1/geo-encoder/regions"
    regions_json = requests.get(regions_api, headers=HEADERS).json()
    for region in regions_json["data"]:
        region_name = region["name"]
        region_slug = region["normalized_name"]
        region_path = f"/uk/{region_slug}/"
        region_url = BASE_URL + region_path
        olx_id = region["id"]
        insert_or_update_region(region_name, region_url, region_slug, region_path, olx_id)

parse_regions()