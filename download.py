from bs4 import BeautifulSoup as bs
import requests
import json
import os
from tqdm import tqdm

from utils import (
    get_category_and_sub_category_hubs,
    get_document_urls_for_section,
    get_next_document_section
)

if __name__ == "__main__":
    domain = "https://www.presidency.ucsb.edu"
    parent_url = domain + "/documents"

    urls_to_visit = get_category_and_sub_category_hubs(parent_url)

    document_urls = {}
    p_bar = tqdm(urls_to_visit.items())
    for (category, sub_category), url_to_hub in p_bar:
            
        url_with_max_results = url_to_hub + "?items_per_page=500"

        parent_html = requests.get(url_with_max_results).text

        soup = bs(parent_html, "html.parser")
        soup = soup.find("section", {"id": "block-system-main"})

        page_document_urls = get_document_urls_for_section(domain, category, sub_category, soup)
        document_urls.update(page_document_urls)
        
        next_document_page = get_next_document_section(domain, soup)
        num_pages_scraped = 1
        while next_document_page is not None:
            num_pages_scraped += 1
            page_document_urls = get_document_urls_for_section(domain, category, sub_category, next_document_page)
            document_urls.update(page_document_urls)
            
            next_document_page = get_next_document_section(domain, next_document_page)
            p_bar.set_postfix({
                "Primary": f"{category}",
                "Sub": f"{sub_category if not None else 'None'}",
                "Num Pages Scraped": f"{num_pages_scraped}"
            })

        # save the document urls to a json file
        with open(os.path.join(os.path.curdir, "document_urls.json"), "w+") as f:
            json.dump(document_urls, f)

    print(len(document_urls))

    # save the document urls to a json file
    with open(os.path.join(os.path.curdir, "document_urls.json"), "w+") as f:
        json.dump(document_urls, f)


