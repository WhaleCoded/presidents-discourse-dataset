import os
import json
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

def parse_html(html_path):
    output = {}
    with open(html_path, "r") as html_file:
        html_data = html_file.read()
        soup = bs(html_data, "html.parser")
        speaker, description, title = get_speaker_description_and_title(soup)
        output["speaker"] = speaker
        output["description"] = description
        output["title"] = title

        body = get_document_body(soup)
        output["body"] = body

        date = get_date(soup)
        output["date"] = date

        citation = get_citation(soup)
        output["citation"] = citation

        footnote = get_footnote(soup)
        output["footnote"] = footnote

        location = get_location(soup)
        output["location"] = location

        media_link = get_media_link(soup)
        output["media_link"] = media_link

    return output

def get_media_link(full_page_soup):
    media_link_soup = full_page_soup.find("div", {"class": "field-docs-media-video-hosted"})
    if media_link_soup is not None:
        if media_link_soup.find("iframe") is not None:
            media_link = media_link_soup.find("iframe").get("src")
            return media_link
        elif media_link_soup.find("a") is not None:
            media_link = media_link_soup.find("a").get("href")
            return media_link
        else:
            raise Exception("No media link found")
    return ""

def get_location(full_page_soup):
    location_soup = full_page_soup.find("div", {"class": "field-docs-location"})
    if location_soup is not None:
        specific_location_soup = location_soup.find("div", {"class": "field-spot-state"})
        if specific_location_soup is not None:
            location = specific_location_soup.text
            return location.replace("\n", "").replace("\t", "")
    return ""
    

def get_footnote(full_page_soup):
    footnote_soup = full_page_soup.find("div", {"class": "field-docs-footnote"})
    if footnote_soup is not None:
        if footnote_soup.find("p") is not None:
            footnote = footnote_soup.find("p").text
            return footnote
    return ""

def get_citation(full_page_soup):
    citation_soup = full_page_soup.find("div", {"class": "field-prez-document-citation"})
    if citation_soup is not None:
        if citation_soup.find("p") is not None:
            citation = citation_soup.find("p").text
            return citation
    return ""

def get_date(soup):
    date_soup = soup.find("div", {"class": "field-docs-start-date-time"})
    date = date_soup.find("span").text
    return date

def get_document_body(full_page_soup):
    body_soup = full_page_soup.find("div", {"class": "field-docs-content"})
    if body_soup is not None:
        p_tags = body_soup.find_all("p")

        body = ""
        for p_tag in p_tags:
            body += p_tag.text
            body += "\n"

        return body

    return ""

def get_speaker_description_and_title(full_page_soup):
    header_soup = full_page_soup.find("div", {"class": "field-docs-person"})

    description = get_speaker_description(header_soup)
    title = get_doc_title(header_soup)
    speaker = get_speaker_name(header_soup)

    return speaker, description, title    

def get_speaker_name(header_soup):
    speaker_soup = header_soup.find("div", {"class": "field-title"})
    speaker_name = speaker_soup.find("a").text
    return speaker_name

def get_speaker_description(header_soup):
    description_soup = header_soup.find("div", {"class": "field-ds-byline"})
    if description_soup is not None:
        if description_soup.find("div", {"class": "diet-by-line"}):
            description_soup = description_soup.find("div", {"class": "diet-by-line"})
            if description_soup.find("span") is not None:
                description = ""
                for span in description_soup.find_all("span"):
                    description += span.text
                    description += " "
                return description
            else:
                description = description_soup.text
                return description
        elif description_soup.find("p") is not None:
            description = description_soup.find("p").text
            return description
    return ""

def get_doc_title(header_soup):
    title_soup = header_soup.find("div", {"class": "field-ds-doc-title"})
    title = title_soup.find("h1").text
    return title

def save_parsed_file(output, file_path):
    with open(file_path, "w+") as f:
        json.dump(output, f)

if __name__ == "__main__":
    SAVE_PATH = os.path.join(os.curdir, os.pardir, "data", "parsed_documents")
    os.makedirs(SAVE_PATH, exist_ok=True)
    CATEGORIES_PATH = os.path.join(os.curdir, os.pardir, "data", "document_urls.json")
    with open(CATEGORIES_PATH, "r") as f:
        categories_by_url = json.load(f)
    SLUGS_PATH = os.path.join(os.curdir, os.pardir, "data", "document_slugs_to_urls.json")
    with open(SLUGS_PATH, "r") as f:
        slugs_to_urls = json.load(f)
    data_path = os.path.join(os.curdir, "data", "html")
    html_paths = [os.path.join(data_path, file_name) for file_name in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, file_name))]

    num_errored = 0
    for html_path in tqdm(html_paths):
        slug = os.path.basename(html_path).replace(".html", "")
        file_path = os.path.join(SAVE_PATH, f"{slug}.json")

        url = slugs_to_urls[slug]
        categories = categories_by_url[url]

        try:
            output = parse_html(html_path)
        except Exception as e:
            print(f"Error parsing {html_path}\n{url}")
            num_errored += 1
        output["categories"] = categories
        output["url"] = url
        output["slug"] = slug
        save_parsed_file(output, file_path)

    print(f"Errored {num_errored} files")







    