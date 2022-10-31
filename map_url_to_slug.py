from utils import convert_url_to_slug
import os
import json

URL_PATHS = os.path.join(os.curdir, "document_urls.json")
DATA_PATH = os.path.join(os.curdir, "data", "html")

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

# Remove extra files
file_paths = [os.path.join(DATA_PATH, file_name) for file_name in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, file_name)) and file_name.endswith(".html")]
num_to_removed = 0
for file_path in file_paths:
    slug = os.path.basename(file_path).replace(".html", "")
    if slug not in slugs_to_urls.keys():
        num_to_removed += 1
        os.remove(file_path)
print(f"Removed {num_to_removed} files")
