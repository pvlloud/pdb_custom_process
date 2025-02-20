import datetime
import json
import pathlib


class FileExporter:
    CHAINS_KEY = "chains"
    DATETIME_FORMAT = "%d-%m-%YT%H:%M:%S"

    def __init__(self, file_name: str, output_directory_name: str = ".") -> None:
        self.file_name = file_name
        self.execution_datetime = datetime.datetime.now()
        self.execution_datetime_string = self.execution_datetime.strftime(
            self.DATETIME_FORMAT
        )
        self.output_directory_name = output_directory_name

    def output_data(self):
        return {
            "file_name": self.file_name,
            "datetime": self.execution_datetime_string,
            self.CHAINS_KEY: {},
        }

    def export_chains_data(self, chains_data: dict) -> dict:
        output_data = self.output_data()
        output_data[self.CHAINS_KEY] = chains_data
        return output_data

    def write_output_file(self, chains_data: dict):
        output_directory = pathlib.Path(self.output_directory_name)
        output_file_name = f"{self.file_name.replace('.', '_')}_{self.execution_datetime_string}_chains.json"
        with open(output_directory / output_file_name, "w") as output_file:
            json.dump(self.export_chains_data(chains_data), output_file)
