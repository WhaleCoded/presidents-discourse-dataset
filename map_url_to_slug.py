from utils import convert_url_to_slug
import os
import json

URL_PATHS = os.path.join(os.curdir, "document_urls.json")

slugs_to_urls = {}
with open(URL_PATHS, "r") as f:
    urls = json.load(f)

    print(f"Number of urls: {len(urls)}")
    for url in urls.keys():
        slug = convert_url_to_slug(url)
        slugs_to_urls[slug] = url
        
print(f"Mapped {len(slugs_to_urls)} slugs to urls")
SAVE_PATH = os.path.join(os.curdir, "document_slugs_to_urls.json")
with open(SAVE_PATH, "w+") as f:
    json.dump(slugs_to_urls, f)