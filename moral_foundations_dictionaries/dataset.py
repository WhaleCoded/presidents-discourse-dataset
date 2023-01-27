import os
import sys
import csv
import random

from tqdm import tqdm
import nltk
from uuid import uuid4


csv.field_size_limit(sys.maxsize)
DEFAULT_SPEECH_PATH = os.path.join(
    "data", "cr_speech_sentences_with_speaker_and_date.csv"
)


class CongressDataset:
    def __init__(
        self,
        path_to_speeches=DEFAULT_SPEECH_PATH,
        date_range=None,
        max_length=None,
        data=None,
    ):
        self.data_path = path_to_speeches
        self.data_range = date_range
        self.max_length = max_length

        # Load data
        if data is None:
            self._load_data()
        else:
            self.data = data

    def _load_data(self):
        data = []

        with open(self.data_path, "r") as f:
            reader = csv.reader(f)

            _ = next(reader)
            for row in tqdm(reader, desc="Loading data"):
                date = int(row[3])
                if (self.data_range is None) or (
                    date >= self.data_range[0] and date <= self.data_range[1]
                ):

                    if self.max_length is not None and len(data) >= self.max_length:
                        break

                    data.append(
                        {
                            "id": row[0],
                            "speech_id": row[1],
                            "speaker": row[2],
                            "date": date,
                            "sentence": row[4:],
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
                date_range=self.data_range,
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

    dataset = CongressDataset(date_range=(2005, 2022))
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
