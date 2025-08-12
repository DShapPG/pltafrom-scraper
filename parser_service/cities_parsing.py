import requests, asyncio, aiohttp
from city import insert_or_update_city
from settings import BASE_URL, HEADERS
from region import get_region_id_by_olx_id, get_all_regions_olx_ids

async def get_lists(session, region_olx_id):
    cities_api = f"https://www.olx.ua/api/v1/geo-encoder/regions/{region_olx_id}/cities/?limit=2000"
    cities = []
    region_id = await get_region_id_by_olx_id(region_olx_id)
    async with session.get(cities_api, headers=HEADERS) as response:
        data = await response.json()


    print(f"REGION: {region_olx_id}")
    for city in data["data"]:
        name = city["name"]
        slug = city["normalized_name"]
        path = f"/{slug}/"
        url = BASE_URL + path
        olx_id = city["id"]

        cities.append((name, url, slug, path, region_id, olx_id))
        print(name)


    await insert_or_update_city(cities)

async def cities_parsing_start():
    olx_ids = await get_all_regions_olx_ids()
    async with aiohttp.ClientSession() as session:
        tasks = [get_lists(session, region_id) for region_id in olx_ids]
        await asyncio.gather(*tasks)


# for region_olx_id in olx_ids:
#     print(f"Parsing city {region_olx_id}")
#     parse_cities(region_olx_id)
#     print("CITY PARSED")
#     time.sleep(1)