from lists import PRESIDENTS, LIWC_DICTIONARIES, PRONOUNS
from dataset import PresidentsDataset
from collections import Counter
from tqdm import tqdm
import csv
import nltk
import os
import json

def reduce_to_nltk_pronouns(tokens):
    pos_tags = nltk.pos_tag(tokens)

    # Remove non-pronouns
    pronoun_tokens = [word.lower() for word, pos in pos_tags if "PRP" in pos or pos == "WP"]

    return pronoun_tokens

def reduce_to_liwc_dictionary(tokens, liwc_dictionary):
    liwc_pronouns = []

    for token in tokens:
        if token.lower() in liwc_dictionary:
            liwc_pronouns.append(token.lower())
        else:
            # Check for tokens with variable endings
            for pronoun in liwc_dictionary:
                if pronoun.endswith("*") and token.lower().startswith(pronoun[:-1]):
                    liwc_pronouns.append(token.lower())
                    break

    return liwc_pronouns

def reduce_to_custom_list(tokens):
    custom_pronouns = []

    for token in tokens:
        if token.lower() in PRONOUNS:
            custom_pronouns.append(token.lower())

    return custom_pronouns

def clean_and_load_dataset():
    dataset = PresidentsDataset()

    # Grab just the presidential documents
    dataset.where(lambda data: "Presidential" in data["categories"]["primary"])
    def thin_data(data):
        return {
            "slug": data["slug"],
            "speaker": data["speaker"].lower(),
            "body": data["body"]
        }
    dataset.map(thin_data)

    return dataset

def get_counts_for_dictionary(cleaned_dataset, dictionary_name, liwc_dictionary, results_path):
    pure_counts_path = os.path.join(results_path, "all_dictionaries", "counts", f"{dictionary_name}_pure_counts.json")
    os.makedirs(os.path.dirname(pure_counts_path), exist_ok=True)

    if not os.path.exists(pure_counts_path):    
        # Count the number of times each pronoun is used by each president
        pronoun_counts = {}
        for data in tqdm(cleaned_dataset, desc="Counting pronouns"):
            speaker = data["speaker"]
            if speaker in PRESIDENTS:
                tokens = nltk.word_tokenize(data["body"])

                # Reduce to LIWC pronouns
                pronoun_tokens = reduce_to_liwc_dictionary(tokens, liwc_dictionary)

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

def save_dictionary_results(dictionary_name, pronoun_counts, results_path):
    results_path = os.path.join(results_path, "all_dictionaries", dictionary_name)
    os.makedirs(results_path, exist_ok=True)

    final_header = set()
    for counter in pronoun_counts.values():
        header = set(counter.keys())
        final_header = final_header.union(header)
    final_header = sorted(list(final_header))

    # Find the most common pronoun for each president
    def get_most_common_pronoun(counter):
        if len(counter) == 0:
            return ""
        return counter.most_common(1)[0][0]

    most_common_pronouns = {}
    for speaker, counter in pronoun_counts.items():
        most_common_pronouns[speaker] = get_most_common_pronoun(counter)

    # Write the president counts to a CSV
    presidents_path = os.path.join(results_path, "presidents.csv")
    with open(presidents_path, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["President"] + ["Most Used Pronoun"] + final_header + ["Total Proportion"])

        cleaned_president_counts = {}
        sorted_names = sorted(list(pronoun_counts.keys()))
        for president, counter in pronoun_counts.items():
            row = [president, most_common_pronouns[president]]

            counts = []
            for header in final_header:
                counts.append(counter[header])
            row += counts + [sum(counts)]
            cleaned_president_counts[president] = row

        #Make sure presidents are in alphabetical order
        for president in sorted_names:
            writer.writerow(cleaned_president_counts[president])

    # Write the pronoun proportions to a CSV
    presidents_prop_path = os.path.join(results_path, "presidents_prop.csv")
    with open(presidents_prop_path, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["President"] + ["Most Used Pronoun"] + final_header + ["Total Pronouns"])

        # Get the total number of words spoken by each president
        total_words = {}
        for president, counter in pronoun_counts.items():
            total_words[president] = sum(counter.values())

        # Write the president counts to a CSV
        proportion_counts = {}
        for president, counter in pronoun_counts.items():
            row = [president, most_common_pronouns[president]]

            props = []
            for header in final_header:
                props.append(counter[header] / total_words[president])

            row = row + props + [sum(props)]
            proportion_counts[president] = row

        #Make sure presidents are in alphabetical order
        for president in sorted_names:
            writer.writerow(proportion_counts[president])

    # Calculate the total pronoun counts
    total_counts = Counter()
    for counter in pronoun_counts.values():
        total_counts += counter
    total_pronoun = sum(total_counts.values())

    total_path = os.path.join(results_path, "total.csv")
    with open(total_path, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["Most Frequently Used Pronoun:"] + [get_most_common_pronoun(total_counts)])
        writer.writerow([])
        writer.writerow(["Pronoun", "Count", "Proportion"])
        for pronoun in final_header:
            writer.writerow([pronoun, total_counts[pronoun], total_counts[pronoun] / total_pronoun])

if __name__ == "__main__":
    results_path = os.path.join(os.path.curdir, os.path.pardir, "results")
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    # Load the presidents dataset
    cleaned_dataset = clean_and_load_dataset()

    for i, (dictionary_name, liwc_dictionary) in enumerate(LIWC_DICTIONARIES.items()):
        print(f"Processing {dictionary_name}-{i+1}/{len(LIWC_DICTIONARIES)}")
        pronoun_counts = get_counts_for_dictionary(cleaned_dataset, dictionary_name, liwc_dictionary, results_path)
        save_dictionary_results(dictionary_name, pronoun_counts, results_path)