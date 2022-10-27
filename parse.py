import os
import json

def parse_and_save_html_files(html_paths, main_category, sub_category, save_path):
    for html_path in html_paths:
        file_name = os.path.basename(html_path).replace(".html", ".json")
        output = parse_html(html_path)


        file_path = os.path.join(save_path, main_category)
        if sub_category is not None:
            file_path = os.path.join(file_path, sub_category)
        file_path = os.path.join(file_path, file_name)
        
        save_parsed_file(output, main_category, sub_category, file_path)

def parse_html(html_path):
    with open(html_path, "r") as html_file:
        html_data = html_file.read()

    return {"Test": "Still need to finish this function"}

def save_parsed_file(output, file_path):
    with open(file_path, "w+") as f:
        json.dump(output, file_path)

if __name__ == "__main__":
    SAVE_PATH = os.path.join(os.curdir, "data", "parsed_documents")
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

        parse_and_save_html_files(html_paths, main_cat_name, None, SAVE_PATH)

        for sub_cat_name, sub_cat_path in sub_category_paths:
            html_paths = []

            for file_name in os.listdir(sub_cat_path):
                curr_path = os.path.join(sub_cat_path, file_name)
                if file_name.endswith(".html") and os.path.isfile(curr_path):
                    html_paths.append(curr_path)

            parse_and_save_html_files(html_paths, main_cat_name, sub_cat_name, SAVE_PATH)








    