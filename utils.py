from bs4 import BeautifulSoup as bs
import requests
import json

def get_category_and_sub_category_hubs(parent_url) -> dict:
    parent_html = requests.get(parent_url).text

    soup = bs(parent_html, "html.parser")
    soup = soup.find("div", {"class": "main-container container"})
    soup = soup.find("section", {"id": "block-system-main"})
    soup = soup.find("ul", {"class": "menu nav"})

    # Get all of the main categories of documents
    urls_to_visit = {}
    categories = soup.findChildren("li", recursive=False)
    for category in categories:
        category_text = category.find("a").text
        category_name = category_text.split(" (")[0]
        num_in_category = int(category_text.split(" (")[1].replace(")", ""))

        category_href = parent_url.replace("/documents", "") + category.find("a")["href"]
        urls_to_visit[(category_name, None)] = category_href

        # Get all of the subcategories of documents
        sub_category_list = category.find("ul", {"class": "dropdown-menu"})
        if sub_category_list is not None:
            sub_categories = sub_category_list.findChildren("li", recursive=False)
            for sub_category in sub_categories:
                sub_category_text = sub_category.find("a").text
                sub_category_name = sub_category_text.split(" (")[0]
                try:
                    num_in_sub_category = int(sub_category_text.split(" (")[1].replace(")", ""))
                except ValueError:
                    num_in_sub_category = int(sub_category_text.split(" (Radio and Webcast) (")[1].replace(")", ""))

                sub_category_href = parent_url.replace("/documents", "") + sub_category.find("a")["href"]
                urls_to_visit[(category_name, sub_category_name)] = sub_category_href

    return urls_to_visit

def get_document_urls_for_section(domain, category, sub_category, section_soup) -> dict:
    page_document_urls = {}
    docu_link_divs = section_soup.find("div", {"class": "view-content"})
    if docu_link_divs is not None:
        docu_a_tags = docu_link_divs.find_all("a")
        for docu_a_tag in docu_a_tags:
            docu_a_tag_url = docu_a_tag["href"]
            if docu_a_tag_url.startswith("/documents"):
                docu_a_tag_url = domain + docu_a_tag_url
                page_document_urls[docu_a_tag_url] = (category, sub_category)

    return page_document_urls

def get_next_document_section(domain, soup):
    next_page_ref = soup.find("a", {"title": "Go to next page"})
    if next_page_ref is not None:
        next_url = domain + next_page_ref["href"]
        parent_html = requests.get(next_url).text
        soup = bs(parent_html, "html.parser")

        return soup.find("section", {"id": "block-system-main"}) if soup is not None else None

    else:
        return None

def hybrid_update(new_urls, old_urls):
    num_duplicates = 0
    num_with_multiple_categories = 0
    for url, (category, sub_category) in new_urls.items():
        if url in old_urls:
            num_duplicates += 1
            category_dict = old_urls[url]
            len_sub = len(category_dict["sub"])
            len_primary = len(category_dict["primary"])
            if sub_category is not None:
                category_dict["sub"].add(sub_category)
            category_dict["primary"].add(category)

            if (len(category_dict["sub"]) > len_sub and len_sub != 0) or len(category_dict["primary"]) > len_primary:
                num_with_multiple_categories += 1
        else:
            if sub_category is not None:
                old_urls[url] = {"primary": set([category]), "sub": set([sub_category])}
            else:
                old_urls[url] = {"primary": set([category]), "sub": set()}

    return old_urls, num_duplicates, num_with_multiple_categories

def save_to_json(data, path):
    # save the document urls to a json file
    with open(path, "w+") as f:
        json_compatible_dict = {}
        for url, category_dict in data.items():
            compatible_dict = {"primary": list(category_dict["primary"]), "sub": list(category_dict["sub"])}
            json_compatible_dict[url] = compatible_dict
        json.dump(json_compatible_dict, f)

def convert_url_to_slug(url):
    URL_START = "https://www.presidency.ucsb.edu/documents/"
    return url.replace(URL_START, "").replace("/", "_").replace(":", "_").replace(".", "_")

    