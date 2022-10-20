from bs4 import BeautifulSoup as bs
import requests

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

    