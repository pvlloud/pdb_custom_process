import json


class GetChainsFromFile:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_chains_iterator(self):
        with open(self.file_path, "r") as f:
            data = json.load(f)

        for chain_id, chain_seq in data["chains"].items():
            yield " ".join(chain_seq)
