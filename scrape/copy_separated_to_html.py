import os
import shutil
from tqdm import tqdm

DESTINATION_PATH = data_path = os.path.join(os.curdir, os.pardir, "data", "html")
os.makedirs(DESTINATION_PATH, exist_ok=True)

def move_separated_to_html(separated_paths):
    for separated_path in separated_paths:
        file_name = os.path.basename(separated_path)
        html_file_path = os.path.join(DESTINATION_PATH, file_name)
        
        shutil.copy(separated_path, html_file_path)

data_path = os.path.join(os.curdir, os.pardir, "data", "separated")
main_category_paths = [(category_name, os.path.join(data_path, category_name))  for category_name in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, category_name))]

for main_cat_name, main_cat_path in tqdm(main_category_paths):
    html_paths = []
    sub_category_paths = []
    for category_name in os.listdir(main_cat_path):
        curr_path = os.path.join(main_cat_path, category_name)
        if os.path.isdir(curr_path):
            sub_category_paths.append((category_name, curr_path))
        elif category_name.endswith(".html"):
            html_paths.append(curr_path)

    move_separated_to_html(html_paths)

    for sub_cat_name, sub_cat_path in sub_category_paths:
        html_paths = []

        for file_name in os.listdir(sub_cat_path):
            curr_path = os.path.join(sub_cat_path, file_name)
            if file_name.endswith(".html") and os.path.isfile(curr_path):
                html_paths.append(curr_path)

        move_separated_to_html(html_paths)