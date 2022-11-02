from lists import PRONOUNS, PRESIDENTS
from dataset import PresidentsDataset
from collections import Counter
from tqdm import tqdm
import csv
import nltk
import os
import json

if __name__ == "__main__":
    results_path = os.path.join(os.path.curdir, os.path.pardir, "results")
    os.makedirs(results_path, exist_ok=True)
    pure_counts_path = os.path.join(results_path, "pure_counts.json")

    if not os.path.exists(pure_counts_path):
        dataset = PresidentsDataset()

        # Grab just the presidential documents
        dataset.where(lambda data: "Presidential" in data["categories"]["primary"])
        def thin_data(data):
            return {
                "slug": data["slug"],
                "speaker": data["speaker"].lower(),
                "body": data["body"].lower()
            }
        dataset.map(thin_data)

        # Count the number of times each pronoun is used by each president
        pronoun_counts = {}
        for data in tqdm(dataset, desc="Counting pronouns"):
            speaker = data["speaker"]
            if speaker in PRESIDENTS:
                tokens = nltk.word_tokenize(data["body"])
                
                # Remove tokens that are not pronouns
                pronoun_tokens = [token for token in tokens if token in PRONOUNS]

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

    
    # Get header for president pronoun counts
    final_header = set()
    for counter in pronoun_counts.values():
        header = set(counter.keys())
        final_header = final_header.union(header)

    final_header = sorted(list(final_header))

    # Write the president counts to a CSV
    presidents_path = os.path.join(results_path, "presidents.csv")
    with open(presidents_path, "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["President"] + final_header)

        cleaned_president_counts = {}
        sorted_names = sorted(list(pronoun_counts.keys()))
        for president, counter in pronoun_counts.items():
            row = [president]
            for header in final_header:
                row.append(counter[header])
            cleaned_president_counts[president] = row

        #Make sure presidents are in alphabetical order
        for president in sorted_names:
            writer.writerow(cleaned_president_counts[president])