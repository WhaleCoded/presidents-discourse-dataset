from bs4 import BeautifulSoup as bs
import requests
import json
import os
from tqdm import tqdm
import time
from utils import convert_url_to_slug


MIN_TIME_BETWEEN_REQUESTS = 0.3

if __name__ == "__main__":

    document_urls_path = os.path.join(os.path.curdir, "document_urls.json")

    with open(document_urls_path, "r") as f:
        document_urls = json.load(f)

    print(f"Number of documents: {len(document_urls)}")

    p_bar = tqdm(document_urls.items())
    num_already_downloaded = 0
    DESTINATION_PATH = os.path.join(os.path.curdir, "data", "html")
    os.makedirs(DESTINATION_PATH, exist_ok=True) 
    for url_to_hub, _ in p_bar:
        start_time = time.time()

        download_destination = os.path.join(DESTINATION_PATH, convert_url_to_slug(url_to_hub) + ".html")

        if not os.path.exists(download_destination):
            document_html = requests.get(url_to_hub).text

            with open(download_destination, "w+") as f:
                f.write(document_html)

            tot_time = time.time() - start_time
            if tot_time < MIN_TIME_BETWEEN_REQUESTS:
                time.sleep(MIN_TIME_BETWEEN_REQUESTS - tot_time)
        else:
            num_already_downloaded += 1
            p_bar.set_postfix({
                "Num Already Downloaded": f"{num_already_downloaded}"
            })

        
