from bs4 import BeautifulSoup as bs
import requests
import json
import os
from tqdm import tqdm


if __name__ == "__main__":

    document_urls_path = os.path.join(os.path.curdir, "data", "document_urls.json")

    with open(document_urls_path, "r") as f:
        document_urls = json.load(f)

    print(f"Number of documents: {len(document_urls)}")

    p_bar = tqdm(document_urls.items())
    num_already_downloaded = 0
    for url_to_hub, (category, sub_category) in p_bar:
        if sub_category is not None:
            download_destination_path = os.path.join(os.path.curdir, "data", "html", category, sub_category)
        else:
            download_destination_path = os.path.join(os.path.curdir, "data", "html", category)

        os.makedirs(download_destination_path, exist_ok=True)
        download_destination = os.path.join(download_destination_path, url_to_hub.replace("/", "_").replace(":", "_").replace(".", "_") + ".html")

        if not os.path.exists(download_destination):
            document_html = requests.get(url_to_hub).text

            with open(download_destination_path, "w+") as f:
                f.write(document_html)
        else:
            num_already_downloaded += 1
            p_bar.set_postfix({
                "Num Already Downloaded": f"{num_already_downloaded}"
            })
