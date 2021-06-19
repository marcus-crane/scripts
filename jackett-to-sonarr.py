"""
Jackett to Sonarr

An extremely sloppy script for inserting Jackett indexes into Sonarr.
If you don't know what that is, you probably don't need it!
I've manually done this setup in the past and it's very tedious
so I decided to automate it once and for all

You can get a Sonarr API key by using the dev tools and checking
the request headers

I might clean this up in future but for now, you'll just have to
manually flip some bits
"""

import json

import requests

sonarr_url = "http://192.168.1.xx:8989"
sonarr_api_key = "<api_key>"

jackett_url = "http://192.168.1.xx:9117"
jackett_api_key = "<api_key>"
jackett_api_url = f"{jackett_url}/api/v2.0/indexers"

test_url = f"{sonarr_url}/api/v3/indexer/test"
submit_url = f"{sonarr_url}/api/v3/indexer"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Sonarr Jackett Sync Script/1.0",
    "X-Api-Key": sonarr_api_key
}

payload = {
    "configContract": "TorznabSettings",
    "enableAutomaticSearch": True,
    "enableInteractiveSearch": True,
    "enableRss": True,
    "implementation": "Torznab",
    "implementationName": "Torznab",
    "infoLink": "https://wiki.servarr.com/Sonarr_Supported_Indexers",
    "priority": 25,
    "protocol": "torrent",
    "supportsRss": True,
    "supportsSearch": True,
    "tags": []
}

fields = [
    { "name": "baseUrl", "value": jackett_url },
    { "name": "apiKey", "value": jackett_api_key },
    { "name": "additionalParameters" },
    { "name": "minimumSeeders", "value": 1 },
    { "name": "seedCriteria.seedRatio" },
    { "name": "seedCriteria.seedTime" },
    { "name": "seedCriteria.seasonPackSeedTime" }
]

r = requests.get(jackett_api_url)
print(r.status_code)
indexers = r.json()
active_indexers = []

tv_numbers = [5000, 5030, 5040, 5080, 100074, 100006, 100009, 100005, 100041, 100071, 100075, 100007, 108346, 120797, 105867, 105503]
anime_numbers = [5070, 100028, 100078, 100079, 100080, 100001, 142158, 122266, 152237, 147671, 120797, 105867, 105503]
movie_numbers = [2000, 2010, 2030, 2040, 2045, 2060, 2070, 100066, 100073, 100002, 100004, 10001, 100054, 100042, 100070, 100055, 100003, 100076, 116972, 120797, 105867, 105503]
anime_movie_numbers = [100028, 100078, 100079, 100080, 100001, 142158, 122266, 152237, 147671, 120797, 105867, 105503]

def submit_indexer(indexer: dict, include_tv_categories=True, include_anime_categories=True, dryrun=True):
    indexer_id = indexer['id']
    indexer_name = indexer['name']
    valid_anime_numbers = list()
    valid_tv_numbers = list()
    for category in indexer['caps']:
        category_id = int(category['ID'])
        if category_id in tv_numbers and include_tv_categories:
            valid_tv_numbers.append(category_id)
        if category_id in anime_numbers and include_anime_categories:
            valid_anime_numbers.append(category_id)
    index_payload = payload.copy()
    index_payload['name'] = indexer_name
    index_fields = fields.copy()
    index_fields.append({
        "name": "apiPath",
        "value": f"/api/v2.0/indexers/{indexer_id}/results/torznab/"
    })
    index_fields.append({
        "name": "categories",
        "value": valid_tv_numbers
    })
    index_fields.append({
        "name": "animeCategories",
        "value": valid_anime_numbers
    })
    index_payload['fields'] = index_fields
    if dryrun:
        r = requests.post(test_url, data=json.dumps(index_payload), headers=headers)
        if r.status_code == 200:
            print(f"Settings for {indexer_name} are valid.")
            return True
        if r.status_code == 400:
            print(f"{indexer_name} threw an error. Perhaps it already exists?")
            print(r.json())
            return False
        return False
    r = requests.post(submit_url, data=json.dumps(index_payload), headers=headers)
    if r.status_code == 201:
        print(f"Successfully added {indexer_name}")

for indexer in indexers:
    if indexer['configured']:
        active_indexers.append(indexer)
        test_result = submit_indexer(
            indexer, include_tv_categories=True,
            include_anime_categories=True, dryrun=True
        )
        if test_result:
            submit_indexer(
                indexer, include_tv_categories=True,
                include_anime_categories=True, dryrun=False)
