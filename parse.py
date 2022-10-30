import os
import json

def parse_and_save_html_files(html_paths, cetegories_by_url, save_path):
    for html_path in html_paths:
        output = parse_html(html_path)

        slug = os.path.basename(html_path).replace(".html", "")
        url = convert_slug_to_url(slug)
        if url not in cetegories_by_url:
            raise Exception(f"URL {url} not found in categories_by_url")
        categories = categories_by_url[url]
        output["categories"] = categories
        output["url"] = url
        output["slug"] = slug


        file_path = os.path.join(save_path, f"{slug}.json")        
        save_parsed_file(output, file_path)

def parse_html(html_path):
    with open(html_path, "r") as html_file:
        html_data = html_file.read()

    return {"Test": "Still need to finish this function"}

def save_parsed_file(output, file_path):
    with open(file_path, "w+") as f:
        json.dump(output, file_path)

def convert_slug_to_url(slug):
    return f"https://www.presidency.ucsb.edu/documents/{slug}"

if __name__ == "__main__":
    SAVE_PATH = os.path.join(os.curdir, "data", "parsed_documents")
    CATEGORIES_PATH = os.path.join(os.curdir, "document_urls.json")
    categories_by_url = json.load(CATEGORIES_PATH)
    data_path = os.path.join(os.curdir, "data", "html")
    main_category_paths = [(category_name, os.path.join(data_path, category_name))  for category_name in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, category_name))]

    for main_cat_name, main_cat_path in main_category_paths:
        html_paths = []
        sub_category_paths = []
        for category_name in os.listdir(main_cat_path):
            curr_path = os.path.join(main_cat_path, category_name)
            if os.path.isdir(curr_path):
                sub_category_paths.append((category_name, curr_path))
            elif category_name.endswith(".html"):
                html_paths.append(curr_path)

        parse_and_save_html_files(html_paths, categories_by_url, SAVE_PATH)

        for sub_cat_name, sub_cat_path in sub_category_paths:
            html_paths = []

            for file_name in os.listdir(sub_cat_path):
                curr_path = os.path.join(sub_cat_path, file_name)
                if file_name.endswith(".html") and os.path.isfile(curr_path):
                    html_paths.append(curr_path)

            parse_and_save_html_files(html_paths, categories_by_url, SAVE_PATH)








    