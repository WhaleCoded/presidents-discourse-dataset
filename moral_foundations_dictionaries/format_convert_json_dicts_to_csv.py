import os
import csv
import json

if __name__ == "__main__":
    JSON_FILE_PATH = os.path.join(os.path.curdir, "json_dicts")

    json_dictionary_file_paths = [
        (os.path.join(JSON_FILE_PATH, file_name), file_name)
        for file_name in os.listdir(JSON_FILE_PATH)
        if ".json" in file_name
    ]

    master_dictionary = {}
    for file_path, file_name in json_dictionary_file_paths:
        with open(file_path, "r") as f:
            dictionary = json.load(f)
            time_period = file_name.split("_")[0]

            for dictionary_name, dictionary_terms in dictionary.items():
                if dictionary_name not in master_dictionary:
                    master_dictionary[dictionary_name] = {}

                master_dictionary[dictionary_name][time_period] = dictionary_terms

    # Sort dictionaries by time period
    for dictionary_name, dictionaries_by_year in master_dictionary.items():
        dictionaries_by_year = {
            k: v
            for k, v in sorted(
                dictionaries_by_year.items(), key=lambda item: item[0], reverse=True
            )
        }
        master_dictionary[dictionary_name] = dictionaries_by_year

    CSV_FILE_PATH = os.path.join(os.path.curdir, "csv_dicts")
    os.makedirs(CSV_FILE_PATH, exist_ok=True)
    for dictionary_name, dictionaries_by_year in master_dictionary.items():
        csv_file_path = os.path.join(CSV_FILE_PATH, f"{dictionary_name}.csv")
        with open(csv_file_path, "w+") as f:
            writer = csv.writer(f)
            writer.writerow(["Time Period", "Dictionary Terms ->"])

            for time_period, dictionary_terms in dictionaries_by_year.items():
                dictionary_terms = sorted(dictionary_terms)
                writer.writerow([time_period] + dictionary_terms)
