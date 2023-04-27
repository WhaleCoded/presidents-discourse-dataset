import os
import sys
import csv
import random
import json

from tqdm import tqdm
import numpy as np

from token_map import TokenMap


csv.field_size_limit(sys.maxsize)
DEFAULT_SPEECH_PATH = os.path.join(
    "data", "cr_speech_sentences_with_speaker_and_date.csv"
)
DEFAULT_FILE_MAP_PATH = os.path.join(
    "data", "cr_speech_sentences_with_speaker_and_date.csv"
)
NUM_SENTENCES = 171890150


class CongressDataset:
    def __init__(
        self,
        token_map: TokenMap,
        path_to_speeches=DEFAULT_SPEECH_PATH,
        date_range=None,
        max_length=None,
        data=None,
        num_sentences=NUM_SENTENCES,
    ):
        self.data_path = path_to_speeches
        self.date_range = date_range
        self.max_length = max_length
        self.token_map = token_map
        self.num_sentences = num_sentences

        self._find_time_period_file()

        # Load data
        if data is None:
            self._load_data()
        else:
            self.data = data

    def _find_time_period_file(self):
        if self.date_range is not None:
            data_dir = os.path.dirname(self.data_path)
            time_period_path = os.path.join(
                data_dir,
                "time_period_data",
                f"{self.date_range[0]}_{self.date_range[1]}_cr_speech_sentences_with_speaker_and_date.csv",
            )

            if os.path.exists(time_period_path):
                self.data_path = time_period_path
                self.using_period_file = True
                return

        self.using_period_file = False

    def _load_data(self):
        data = []

        with open(self.data_path, "r") as f:
            reader = csv.reader(f)

            _ = next(reader)
            if self.using_period_file:
                pbar = tqdm(reader, desc="Loading time_period data")
            else:
                pbar = tqdm(reader, desc="Loading data", total=self.num_sentences)

            for row in pbar:
                date = int(row[3])
                if (self.date_range is None) or (
                    date >= self.date_range[0] and date <= self.date_range[1]
                ):

                    if self.max_length is not None and len(data) >= self.max_length:
                        break

                    # Convert sentence to numpy array to save memory
                    # sentence_np_array = np.zeros(len(row[4:]), dtype=np.uint32)
                    sentence_np_array = [0 for _ in row[4:]]
                    for i, token in enumerate(row[4:]):
                        token_id = self.token_map.get_token_id_from_token(token)
                        sentence_np_array[i] = token_id

                    data.append(
                        {
                            "id": row[0],
                            "speech_id": row[1],
                            "speaker": row[2],
                            "date": date,
                            "sentence": sentence_np_array,
                        }
                    )

        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index) -> dict:
        return self.data[index]

    def truncate(self, max_length):
        self.data = self.data[:max_length]

    def shuffle(self):
        random.shuffle(self.data)

    def where(self, condition, remove_in_place=True):
        if remove_in_place:
            self.data = [data for data in self.data if condition(data)]
        else:
            filtered_data = [data for data in self.data if condition(data)]
            return CongressDataset(
                path_to_speeches=self.data_path,
                date_range=self.date_range,
                max_length=self.max_length,
                data=filtered_data,
            )

    def map(self, func, verbose=False):
        if verbose:
            self.data = [func(data) for data in tqdm(self.data, desc="Mapping")]
        else:
            self.data = [func(data) for data in self.data]

    def __iter__(self):
        return iter(self.data)


if __name__ == "__main__":
    import collections

    dataset = CongressDataset(date_range=(2000, 2022))
    print(len(dataset))

    # Test iterator works
    date_counts = {}
    for data in tqdm(dataset):
        if data["date"] not in date_counts:
            date_counts[data["date"]] = 0

        date_counts[data["date"]] += 1
    date_counts = collections.OrderedDict(sorted(date_counts.items()))
    print(date_counts)

    # Filter with lambda function
    def find_certain_time_period(data):
        if data["date"] >= 1873 and data["date"] <= 1874:
            return True

    # dataset = CongressDataset()
    dataset.where(find_certain_time_period)
    print(len(dataset))
