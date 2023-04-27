import csv
import os

from tqdm import tqdm


def _load_speech_meta_data(path_to_meta_data):
    speech_meta_data = {}

    with open(path_to_meta_data, "r") as f:
        reader = csv.reader(f)

        _ = next(reader)

        for row in tqdm(reader, desc="Loading speech meta data"):
            speech_id = row[0]
            speech_date = row[2]

            try:
                speech_date = int(speech_date[0:4])
            except ValueError:
                speech_date = None

            speech_speaker = row[6]
            speech_meta_data[speech_id] = {
                "date": speech_date,
                "speaker": speech_speaker,
            }

    return speech_meta_data


if __name__ == "__main__":
    PATH_TO_SENETENCES = os.path.join("cr_speech_sentences.csv")
    PATH_TO_META_DATA = os.path.join("cr_descriptions.csv")
    SAVE_PATH = os.path.join("cr_speech_sentences_with_speaker_and_date.csv")

    speech_meta_data = _load_speech_meta_data(PATH_TO_META_DATA)

    with open(PATH_TO_SENETENCES, "r") as f:
        reader = csv.reader(f)

        header = next(reader)
        with open(SAVE_PATH, "w+") as save_file:
            writer = csv.writer(save_file)

            writer.writerow(["id", "speech_id", "speaker", "date", "sentence ->"])

            for row in tqdm(reader, desc="Adding speaker and date"):
                sentence_id = row[0]
                speech_id = row[1]

                if speech_id in speech_meta_data:
                    speaker = speech_meta_data[speech_id]["speaker"]
                    date = speech_meta_data[speech_id]["date"]

                    writer.writerow([sentence_id, speech_id, speaker, date] + row[2:])
