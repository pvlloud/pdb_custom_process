import json
from pathlib import Path

import numpy as np


class PredictionFileExporter:
    def __init__(self, file_name, output_directory_name=".") -> None:
        self.file_name = file_name
        self.json_file_name = f"{self.file_name}.json"
        self.output_directory_path = Path(output_directory_name)
        self.output_file_path = self.output_directory_path / self.json_file_name
        self.sequence_embedding_file_name = f"{self.file_name}_sequence_embedding.npy"
        self.sequence_embedding_file_path = (
            self.output_directory_path / self.sequence_embedding_file_name
        )

    def export_prediction_results(self, prediction_results: dict):
        sequence_embedding = prediction_results.pop("raw_sequence_embedding")
        with open(self.output_file_path, "w") as json_file:
            json.dump(prediction_results, json_file, indent=4)
        np.save(self.sequence_embedding_file_path, sequence_embedding)
