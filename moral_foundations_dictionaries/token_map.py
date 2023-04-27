import os
import csv
import json
import re

from tqdm import tqdm

NUM_SENTENCES = 171890150


def create_re_from_formatted_dictionary(formatted_dict_path: os.PathLike):
    with open(formatted_dict_path, "r") as f:
        formatted_dict = json.load(f)

    # Find all tokens that need to be converted to regular expressions
    tokens_that_need_re = set()
    for term_list in formatted_dict.values():
        for term in term_list:
            if "*" in term:
                tokens_that_need_re.add(term.replace(" ", ""))
    tokens_that_need_re = list(tokens_that_need_re)

    re_string = "|".join([token.replace("*", ".*?") for token in tokens_that_need_re])

    if re_string == "":
        return None

    return re.compile(re_string)


class TokenMap:
    def __init__(
        self,
        path_to_sentences: os.PathLike,
        save_path: os.PathLike,
        dictionary_re=None,
        num_sentences: int = NUM_SENTENCES,
        additional_corpus=None,
    ):
        self.tokens_file_name = "tokens.json"
        self.ids_file_name = "ids.json"
        self.dictionary_re_file_name = "dictionary_re_string.txt"

        self.unkown_token = "<UNK>"
        self.unkown_id = 0

        self.csv_path = path_to_sentences
        self.num_sentences = num_sentences
        self.dictionary_re = dictionary_re
        self.save_path = save_path
        self.unique_additional_corpus_tokens = set()

        if os.path.exists(
            os.path.join(save_path, self.tokens_file_name)
        ) and os.path.exists(os.path.join(save_path, self.ids_file_name)):
            print("Loading token map from disk...")
            self._load()
        else:
            os.makedirs(save_path, exist_ok=True)

            self._create_token_map()

            if additional_corpus is not None:
                self._add_tokens_from_corpus(additional_corpus)

            self._save()

    def _save(self):
        tokens_file_path = os.path.join(self.save_path, self.tokens_file_name)
        ids_file_path = os.path.join(self.save_path, self.ids_file_name)

        with open(tokens_file_path, "w+") as f:
            json.dump(self.tokens_to_id, f)

        with open(ids_file_path, "w+") as f:
            json.dump(self.ids_to_token, f)

        if self.dictionary_re is not None:
            re_file_path = os.path.join(self.save_path, self.dictionary_re_file_name)
            with open(re_file_path, "w+") as f:
                f.write(self.dictionary_re.pattern)

    def _load(self):
        tokens_file_path = os.path.join(self.save_path, self.tokens_file_name)
        ids_file_path = os.path.join(self.save_path, self.ids_file_name)

        with open(tokens_file_path, "r") as f:
            self.tokens_to_id = json.load(f)
            self.tokens_to_id = {k: int(v) for k, v in self.tokens_to_id.items()}

        with open(ids_file_path, "r") as f:
            self.ids_to_token = json.load(f)
            self.ids_to_token = {int(k): v for k, v in self.ids_to_token.items()}

        dictionary_re_file_path = os.path.join(
            self.save_path, self.dictionary_re_file_name
        )

        if os.path.exists(dictionary_re_file_path):
            with open(dictionary_re_file_path, "r") as f:
                self.dictionary_re = re.compile(f.read())

    def _calc_term_frequencies(self):
        token_frequencies = {}
        with open(self.csv_path, "r") as f:
            reader = csv.reader(f)
            header = next(reader)

            for row in tqdm(
                reader, total=self.num_sentences, desc="Creating token map"
            ):
                sentence = row[4:]
                for token in sentence:
                    if self.dictionary_re is not None:
                        # We need to translate the appropriate tokens to their
                        # regular expression equivalents
                        match = self.dictionary_re.match(token)
                        if match:
                            token = match[0] + "*"

                    if token not in token_frequencies:
                        token_frequencies[token] = 0

                    token_frequencies[token] += 1

        # Sort the tokens by frequency
        return sorted(token_frequencies, key=token_frequencies.get, reverse=True)

    def _create_token_map(self):
        tokens_to_id = {self.unkown_token: self.unkown_id}
        ids_to_token = {self.unkown_id: self.unkown_token}

        curr_token_id = 1
        token_frequencies = self._calc_term_frequencies()

        # We assign the tokens that are most frequent the lowest token ids
        # This would help us save space if python actually let us choose the size on ints lol
        for token in token_frequencies:
            tokens_to_id[token] = curr_token_id
            ids_to_token[curr_token_id] = token
            curr_token_id += 1

        self.tokens_to_id = tokens_to_id
        self.ids_to_token = ids_to_token

    def _add_tokens_from_corpus(self, corpus):
        curr_max_token_id = max(self.tokens_to_id.values())

        for cor_token in corpus:
            if cor_token not in self.tokens_to_id:
                curr_max_token_id += 1
                self.tokens_to_id[cor_token] = curr_max_token_id
                self.ids_to_token[curr_max_token_id] = cor_token
                self.unique_additional_corpus_tokens.add(curr_max_token_id)

    def token_id_unique_to_additional_corpus(self, token_id):
        return token_id in self.unique_additional_corpus_tokens

    def get_num_unique_tokens(self):
        return len(self.tokens_to_id.keys())

    def get_token_id_from_token(self, token: str):
        if token in self.tokens_to_id:
            return self.tokens_to_id[token]
        elif self.dictionary_re is not None:
            try:
                match = self.dictionary_re.match(token)
            except TypeError as e:
                print(f"Error matching token: {token}")
                raise e
            if match:
                formatted_match = match[0] + "*"
                if formatted_match in self.tokens_to_id:
                    return self.tokens_to_id[formatted_match]
                else:
                    print(f"Token matched but not in dict: {formatted_match}")

        return self.unkown_id

    def get_token_from_id(self, token_id: int):
        if token_id in self.ids_to_token:
            return self.ids_to_token[token_id]
        else:
            print(f"token id was not present in dict: {token_id}")
            return self.unkown_token


if __name__ == "__main__":
    DATA_PATH = os.path.join(
        os.path.curdir, "data", "cr_speech_sentences_with_speaker_and_date.csv"
    )
    FORMATTED_DICT_PATH = os.path.join(
        os.path.curdir,
        "data",
        "original_moral_foundation_dicts",
        "congressional_formatted_dict.json",
    )
    SAVE_PATH = os.path.join(os.path.curdir, "data", "token_map")

    dictionary_re = create_re_from_formatted_dictionary(FORMATTED_DICT_PATH)

    token_map = TokenMap(DATA_PATH, SAVE_PATH, dictionary_re=dictionary_re)

    print(token_map.get_num_unique_tokens())
    print(token_map.get_token_from_id(0))
    print(token_map.get_token_from_id(10))
