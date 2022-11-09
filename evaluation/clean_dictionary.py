# We are converting the liwc dictionary to a tidy format
import csv
import os
import numpy as np

RAW_LIWC_PATH = os.path.join(os.path.curdir, "raw_all_liwc_dictionaries.csv")

with open(RAW_LIWC_PATH, "r") as f:
    reader = csv.reader(f)

    header_row = next(reader)[1:]
    dictionary_names = []

    # Get dictionary names and start and stop indexes
    for i, entry in enumerate(header_row):
        if entry == "":
            continue
        dictionary_names.append((entry, i))

    for i in range(len(dictionary_names)):
        if i == len(dictionary_names) - 1:
            dictionary_names[i] = (dictionary_names[i][0], dictionary_names[i][1], dictionary_names[i][1] + 1)
            continue

        # get start and end index of each dictionary
        dictionary_names[i] = (dictionary_names[i][0], dictionary_names[i][1], dictionary_names[i+1][1] - 1)

    # remove white space
    next(reader)
    next(reader)
    next(reader)

    # gather entries
    dictionary_entries = []
    for row in reader:
        dictionary_entries.append(row[1:])

    # flatten the dictionary entries
    dictionary_entries = np.array(dictionary_entries)
    cleaned_dictionary_entries = {}
    for dataset_name, start, end in dictionary_names:
        dictionary = dictionary_entries[:, start:end].flatten()
        dictionary = [entry for entry in dictionary if entry != ""]
        dictionary = sorted(dictionary)

        cleaned_dictionary_entries[dataset_name] = dictionary

    # write to file
    CLEANED_LIWC_PATH = os.path.join(os.path.curdir, "cleaned_liwc_dictionaries.csv")
    with open(CLEANED_LIWC_PATH, "w+") as f:
        csv_writer = csv.writer(f)

        for dataset_name, dictionary in cleaned_dictionary_entries.items():
            csv_writer.writerow([dataset_name] + dictionary)


    



