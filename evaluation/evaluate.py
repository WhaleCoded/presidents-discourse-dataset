import os
import json
import csv
from collections import Counter
import multiprocessing as mp
import re

from tqdm import tqdm
import nltk

from lists import PRESIDENTS, LIWC_DICTIONARIES
from dataset import PresidentsDataset


def create_re_from_dictionary(liwc_dictionary):
    tokens_that_need_re = [token for token in liwc_dictionary if "*" in token]
    re_string = "|".join(
        ["\b" + token.replace("*", ".*?") + "\b" for token in tokens_that_need_re]
    )

    return re.compile(re_string)


def clean_and_load_dataset():
    dataset = PresidentsDataset()

    # Grab just the documents in the presidential category and presidential speaker
    dataset.where(
        lambda data: "Presidential" in data["categories"]["primary"]
        and data["speaker"].lower() in PRESIDENTS
    )

    def thin_data(data):
        return {
            "slug": data["slug"],
            "speaker": data["speaker"].lower(),
            "body": data["body"],
        }

    dataset.map(thin_data)

    return dataset


# This function uses nltk to tokenize and counts the lowercase version of the tokens
def tokenize_and_count_all_documents(cleaned_dataset):
    token_counts_by_president = {}
    for president in PRESIDENTS:
        token_counts_by_president[president] = Counter()

    # Tokenize and count all documents
    for data in tqdm(cleaned_dataset, desc="Tokenizing and counting all documents"):
        tokens = nltk.word_tokenize(data["body"])
        tokens = [token.lower() for token in tokens]
        token_counter = Counter(tokens)

        token_counts_by_president[data["speaker"]] += token_counter

    return token_counts_by_president


def reduce_to_liwc_dictionary(token_counts, liwc_dictionary, available_re):
    available_tokens = token_counts.keys()
    liwc_entries = Counter()

    for token in available_tokens:
        if token in liwc_dictionary:
            liwc_entries[token] += token_counts[token]
        else:
            # Check for tokens with variable endings
            match = available_re.match(token)
            if match:
                # Multiple token counts will match, so we need to keep a running total
                if match[0] not in liwc_entries:
                    liwc_entries[match[0]] = 0

                liwc_entries[match[0]] += token_counts[token]

    return liwc_entries


def get_counts_for_dictionary(
    cleaned_dataset, dictionary_name, dict_index, liwc_dictionary, results_path
):
    pure_counts_path = os.path.join(
        results_path,
        "all_dictionaries",
        "counts",
        f"{dictionary_name}_pure_counts.json",
    )
    os.makedirs(os.path.dirname(pure_counts_path), exist_ok=True)

    if not os.path.exists(pure_counts_path):
        # Count the number of times each pronoun is used by each president
        pronoun_counts = {}
        dictionary_re = create_re_from_dictionary(liwc_dictionary)
        for data in tqdm(
            cleaned_dataset,
            desc=f"Counting {dictionary_name}-{dict_index + 1}/{len(LIWC_DICTIONARIES)}",
        ):
            speaker = data["speaker"]
            if speaker in PRESIDENTS:
                tokens = nltk.word_tokenize(data["body"])

                # Reduce to LIWC pronouns
                pronoun_tokens, dictionary_re = reduce_to_liwc_dictionary(
                    tokens, liwc_dictionary, dictionary_re
                )

                # Keep running total of pronoun counts
                if speaker not in pronoun_counts:
                    pronoun_counts[speaker] = Counter()
                pronoun_counts[speaker] += Counter(pronoun_tokens)

        # Save the counts
        with open(pure_counts_path, "w+") as f:
            undo_counter = {}
            for speaker, counter in pronoun_counts.items():
                undo_counter[speaker] = [e for e in counter.elements()]
            json.dump(undo_counter, f)
    else:
        print("Counts were already calculated. Loading from file.")
        with open(pure_counts_path, "r") as f:
            pronoun_counts = json.load(f)
            for speaker, elements in pronoun_counts.items():
                pronoun_counts[speaker] = Counter(elements)

    return pronoun_counts


def get_entry_header(dictionary_entry_counts):
    final_header = set()
    for counter in dictionary_entry_counts.values():
        header = set(counter.keys())
        final_header = final_header.union(header)
    final_header = sorted(list(final_header))

    return final_header


def get_most_common_entry(counter):
    if len(counter) == 0:
        return ""
    return counter.most_common(1)[0][0]


def save_raw_president_results(entry_counts, most_common_entries, header, save_path):
    save_path = os.path.join(save_path, "raw_president_counts.csv")

    with open(save_path, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["President"] + ["Most Used Pronoun"] + header + ["Total"])

        cleaned_president_counts = {}
        sorted_names = sorted(list(entry_counts.keys()))
        for president, counter in entry_counts.items():
            row = [president, most_common_entries[president]]

            counts = []
            for header_entry in header:
                counts.append(counter[header_entry])
            row += counts + [sum(counts)]
            cleaned_president_counts[president] = row

        # Make sure presidents are in alphabetical order
        for president in sorted_names:
            writer.writerow(cleaned_president_counts[president])


def save_normalized_president_results(
    entry_counts, most_common_entries, header, save_path
):
    save_path = os.path.join(save_path, "normalized_president_counts.csv")
    with open(save_path, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["President"] + ["Most Used Pronoun"] + header + ["Total Proportion"]
        )

        # Get the total number of words spoken by each president
        total_words = {}
        for president, counter in entry_counts.items():
            total_words[president] = sum(counter.values())

        # Write the president counts to a CSV
        proportion_counts = {}
        sorted_names = sorted(list(entry_counts.keys()))
        for president, counter in entry_counts.items():
            row = [president, most_common_entries[president]]

            props = []
            for header_entry in header:
                if total_words[president] == 0:
                    props.append(0)
                else:
                    props.append(counter[header_entry] / total_words[president])

            row = row + props + [sum(props)]
            proportion_counts[president] = row

        # Make sure presidents are in alphabetical order
        for president in sorted_names:
            writer.writerow(proportion_counts[president])


def save_total_entry_results(entry_counts, header, save_path):
    save_path = os.path.join(save_path, "total_counts.csv")

    # Calculate the total entries counts
    total_counts = Counter()
    for counter in entry_counts.values():
        total_counts += counter
    total_num_entries = sum(total_counts.values())

    with open(save_path, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Most Frequently Used Pronoun:"] + [get_most_common_entry(total_counts)]
        )
        writer.writerow([])
        writer.writerow(["Pronoun", "Count", "Proportion"])
        for entry in header:
            writer.writerow(
                [
                    entry,
                    total_counts[entry],
                    total_counts[entry] / total_num_entries,
                ]
            )

        writer.writerow([])
        writer.writerow(["Total", total_num_entries, 1])


def save_dictionary_results(config, save_path):
    dictionary_name = config["dictionary_name"]
    entry_counts_by_president = config["entry_counts_by_president"]

    results_path = os.path.join(save_path, "all_dictionaries", dictionary_name)
    os.makedirs(results_path, exist_ok=True)

    final_header = get_entry_header(entry_counts_by_president)

    most_common_pronouns = {}
    for speaker, counter in entry_counts_by_president.items():
        most_common_pronouns[speaker] = get_most_common_entry(counter)

    # Save different variations of the results
    save_raw_president_results(
        entry_counts_by_president, most_common_pronouns, final_header, results_path
    )

    save_normalized_president_results(
        entry_counts_by_president, most_common_pronouns, final_header, results_path
    )

    save_total_entry_results(entry_counts_by_president, final_header, results_path)


def run_counts_for_dictionary(config):
    token_counts_by_president = config["token_counts_by_president"]
    lwic_dictionary = config["liwc_dictionary"]
    availabel_re = create_re_from_dictionary(lwic_dictionary)

    # Reduce to LIWC entries
    lwic_entries_by_president = {}
    for president, token_counts in token_counts_by_president.items():
        lwic_entries_by_president[president] = reduce_to_liwc_dictionary(
            token_counts, lwic_dictionary, availabel_re
        )

    return {
        "entry_counts_by_president": lwic_entries_by_president,
        "dictionary_name": config["dictionary_name"],
    }


def dictionary_analysis_generator():
    p_bar = tqdm(total=len(LIWC_DICTIONARIES))

    # Calculate or load the token counts
    path_to_all_tokens = os.path.join(
        os.path.curdir,
        os.pardir,
        "data",
        "all_president_tokens",
        "all_president_tokens.json",
    )
    os.makedirs(os.path.dirname(path_to_all_tokens), exist_ok=True)

    if os.path.exists(path_to_all_tokens):
        with open(path_to_all_tokens, "r") as f:
            all_tokens = json.load(f)

        token_counts_by_president = {}
        for president, tokens in all_tokens.items():
            president_counter = Counter()
            for token, count in tokens.items():
                president_counter[token] = count

            token_counts_by_president[president] = president_counter
    else:
        p_bar.set_postfix_str("Cleaning and Loading President Data")
        cleaned_dataset = clean_and_load_dataset()
        p_bar.set_postfix_str("Tokenizing President Data")
        token_counts_by_president = tokenize_and_count_all_documents(cleaned_dataset)

        # Save the token counts
        with open(path_to_all_tokens, "w+") as f:
            json.dump(token_counts_by_president, f)

    p_bar.set_postfix_str("Analyzing Dictionaries")
    for dictionary_name, lwic_dictionary in LIWC_DICTIONARIES.items():
        config = {}
        config["token_counts_by_president"] = token_counts_by_president
        config["liwc_dictionary"] = lwic_dictionary
        config["dictionary_name"] = dictionary_name

        yield config

        p_bar.update(1)


if __name__ == "__main__":
    MAX_WORKERS = mp.cpu_count() - 1
    MULTI_PROCESSING = True
    SAVE_PATH = os.path.join(
        os.path.curdir, os.path.pardir, "results", "word_boundary_multi_re"
    )

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", default=SAVE_PATH)
    parser.add_argument("--multi_processing", type=bool, default=MULTI_PROCESSING)
    parser.add_argument("--num_threads", type=int, default=MAX_WORKERS)
    args = vars(parser.parse_args())
    os.makedirs(args["save_path"], exist_ok=True)

    if not args["multi_processing"]:
        num_threads = 1
    else:
        num_threads = args["num_threads"]

    with mp.Pool(num_threads, maxtasksperchild=1) as pool:
        results = pool.imap_unordered(
            run_counts_for_dictionary, dictionary_analysis_generator()
        )

        # This starts the analysis and saves the results as they are completed
        for result in results:
            save_dictionary_results(result, args["save_path"])

    # Load the presidents dataset
    # cleaned_dataset = clean_and_load_dataset()

    # # Create Thread Pool
    # pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    # def task(
    #     cleaned_dataset, dictionary_name, dict_index, liwc_dictionary, results_path
    # ):
    #     # print(f"Processing {dictionary_name}-{dict_index+1}/{len(LIWC_DICTIONARIES)}")
    #     pronoun_counts = get_counts_for_dictionary(
    #         cleaned_dataset, dictionary_name, dict_index, liwc_dictionary, results_path
    #     )
    #     save_dictionary_results(dictionary_name, pronoun_counts, results_path)

    # for i, (dictionary_name, liwc_dictionary) in enumerate(LIWC_DICTIONARIES.items()):
    #     if MULTI_PROCESSING:
    #         pool.submit(
    #             task, cleaned_dataset, dictionary_name, i, liwc_dictionary, results_path
    #         )
    #     else:
    #         task(cleaned_dataset, dictionary_name, i, liwc_dictionary, results_path)
