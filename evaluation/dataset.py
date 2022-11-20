import os
from tqdm import tqdm
import json
import random

DEFAULT_PATH = os.path.join(os.path.curdir, os.path.pardir, "data", "parsed_documents")


class PresidentsDataset:
    def __init__(
        self,
        path_to_data=DEFAULT_PATH,
        primary_categories=None,
        sub_categories=None,
        max_length=None,
    ):
        self.path_to_data = path_to_data
        self.max_length = max_length

        # Store filtering conditions
        if primary_categories is not None:
            self.primary_categories = set(primary_categories)
        else:
            self.primary_categories = None
        if sub_categories is not None:
            self.sub_categories = set(sub_categories)
        else:
            self.sub_categories = None

        # Load data
        self._load_data()

    def _load_data(self):
        data = []

        file_paths = [
            os.path.join(self.path_to_data, file_name)
            for file_name in os.listdir(self.path_to_data)
            if os.path.isfile(os.path.join(self.path_to_data, file_name))
            and file_name.endswith(".json")
        ]
        for file_path in tqdm(file_paths, desc="Loading data"):
            with open(file_path, "r") as f:
                json_data = json.load(f)

                # Load only the data from the categories specified
                if self.primary_categories is None and self.sub_categories is None:
                    data.append(json_data)
                elif self.primary_categories is not None:
                    if all(
                        [
                            category in json_data["categories"]["primary"]
                            for category in self.primary_categories
                        ]
                    ):
                        data.append(json_data)
                elif all(
                    [
                        category in json_data["categories"]["sub"]
                        for category in self.sub_categories
                    ]
                ):
                    if json_data["categories"]["sub"] in self.sub_categories:
                        data.append(json_data)

            if self.max_length is not None and len(data) >= self.max_length:
                break

        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index) -> dict:
        return self.data[index]

    def truncate(self, max_length):
        self.data = self.data[:max_length]

    def shuffle(self):
        random.shuffle(self.data)

    def where(self, condition):
        self.data = [data for data in self.data if condition(data)]

    def map(self, func, verbose=False):
        if verbose:
            self.data = [func(data) for data in tqdm(self.data, desc="Mapping")]
        else:
            self.data = [func(data) for data in self.data]

    def __iter__(self):
        return iter(self.data)


if __name__ == "__main__":
    dataset = PresidentsDataset()
    print(len(dataset))

    # Filter by primary category
    dataset = PresidentsDataset(primary_categories=["Presidential"])
    print(len(dataset))

    # Filter with lambda function
    def find_presidential(data):
        if "Presidential" in data["categories"]["primary"]:
            return True

    dataset = PresidentsDataset()
    dataset.where(find_presidential)
    print(len(dataset))

    # Test iterator works
    for data in tqdm(dataset):
        pass
