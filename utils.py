import json


def get_mapping_dict_from_file(file_path: "str") -> dict:
    with open(file_path, "r") as mapping_file:
        return json.load(mapping_file)
