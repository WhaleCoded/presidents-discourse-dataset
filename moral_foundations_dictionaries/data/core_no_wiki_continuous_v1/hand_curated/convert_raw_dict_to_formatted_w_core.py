import os
import csv
import json
from typing import List


def put_term_in_correct_dictionaries(
    csv_row: List[str],
    dict_name_to_tokens: dict,
    dict_id_to_name: dict,
    core_terms: set,
):
    if len(csv_row) >= 2 and csv_row[0] != "":
        term = csv_row[0].replace(" ", "")
        core = True if csv_row[1] == "0" else False
        if core:
            core_terms.add(term)

        for dict_id in csv_row[2:]:
            if dict_id == "":
                continue

            dict_name = dict_id_to_name[int(dict_id)]
            if dict_name not in dict_name_to_tokens:
                dict_name_to_tokens[dict_name] = set()

            dict_name_to_tokens[dict_name].add(term)

    return dict_name_to_tokens, core_terms


def format_raw_dict(
    raw_dict_path: os.PathLike,
    formatted_dict_path: os.PathLike,
    core_terms_path: os.PathLike,
):
    with open(raw_dict_path, "r") as raw_dict:
        reader = csv.reader(raw_dict, delimiter="\t")
        dict_id_to_name = {}
        dict_name_to_tokens = {}
        core_tokens = set()

        # Get dictionary names and ids
        dict_id_to_name = {
            1: "Harm",
            2: "Harm",
            3: "Fairness",
            4: "Fairness",
            5: "Ingroup",
            6: "Ingroup",
            7: "Authority",
            8: "Authority",
            9: "Institutional_Purity",
            10: "Institutional_Purity",
            11: "Sexual_Purity",
            12: "Sexual_Purity",
        }
        dict_ids_start = False
        temp_row = next(reader)
        while not dict_ids_start or (len(temp_row) > 0 and temp_row[0] != "%"):
            if len(temp_row) > 0:
                if temp_row[0] == "%" and not dict_ids_start:
                    dict_ids_start = True
                # elif dict_ids_start:
                #     dict_id = temp_row[0][0:2]
                #     dict_id = int(dict_id)

                #     dict_name = temp_row[0][2:].replace(" ", "")

                #     dict_id_to_name[dict_id] = dict_name

            temp_row = next(reader)
        print(dict_id_to_name)

        # Store dictionary terms in correct dictionaries
        for row in reader:
            if len(row) == 0:
                continue
            elif row[0] == "":
                continue
            elif row[0] == "stem":
                continue

            dict_name_to_tokens, core_tokens = put_term_in_correct_dictionaries(
                row, dict_name_to_tokens, dict_id_to_name, core_terms=core_tokens
            )

        with open(formatted_dict_path, "w+") as formatted_dict:
            # You cannot serialize sets, so we convert them to lists
            for dict_name, term_set in dict_name_to_tokens.items():
                dict_name_to_tokens[dict_name] = sorted(list(term_set))
            json.dump(dict_name_to_tokens, formatted_dict)

        with open(core_terms_path, "w+") as core_terms_file:
            json.dump({"core": list(core_tokens)}, core_terms_file)


if __name__ == "__main__":
    DICT_PATH = os.path.join(os.path.curdir, "core_w_hand_curated.csv")
    FORMATTED_DICT_PATH = os.path.join(
        os.path.curdir, "formatted_hand_curated_dict.json"
    )
    CORE_TERMS_PATH = os.path.join(os.path.curdir, "core_terms.json")

    format_raw_dict(DICT_PATH, FORMATTED_DICT_PATH, CORE_TERMS_PATH)
