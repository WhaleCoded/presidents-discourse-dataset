import csv
import os
import sys

from tqdm import tqdm
import nltk
from uuid import uuid4

csv.field_size_limit(sys.maxsize)


def _split_speech_into_sentences(speech):
    cleaned_and_tokenized_speech = []
    sentences = nltk.sent_tokenize(speech)

    for sentence in sentences:
        word_holder = []
        for word in nltk.word_tokenize(sentence):
            word_holder.append(word.lower())

        if len(word_holder) > 2:
            cleaned_and_tokenized_speech.append(word_holder)

    return cleaned_and_tokenized_speech


if __name__ == "__main__":
    PATH_TO_SPEECHES = os.path.join("cr_speeches.csv")
    SAVE_PATH = os.path.join("cr_speech_sentences.csv")
    TOT_SPEECHES = 17_698_964

    with open(PATH_TO_SPEECHES, "r") as f:
        reader = csv.reader(f)

        header = next(reader)
        with open(SAVE_PATH, "w+") as save_file:
            writer = csv.writer(save_file)

            writer.writerow(["id", "speech_id", "sentence ->"])

            for row in tqdm(
                reader, desc="Loading and cleaning speeches", total=TOT_SPEECHES
            ):
                speech_id = row[0]
                speech_text = row[1]

                # This appears to be important to the nltk sentence tokenize
                speech_text = speech_text.replace("\n", " ")

                sentences = _split_speech_into_sentences(speech_text)
                for sentence in sentences:
                    writer.writerow([str(uuid4()), speech_id] + sentence)
