from pathlib import Path

from environs import Env

from celery_app import app
from exporters.chain_file_exporter import FileExporter
from exporters.prediction_file_exporter import PredictionFileExporter
from file_providers.chain_provider import GetChainsFromFile
from file_providers.local_file_provider import LocalFileProvider
from model_processors.t5_model_executor import T5ModelExecutor
from pdb_processors.pdb_custom_processor import PDBFileProcessor

env = Env()

INPUT_FOLDER_NAME = env.str("INPUT_FOLDER_NAME")
OUTPUT_DIRECTORY_NAME = env.str("OUTPUT_DIRECTORY_NAME")


@app.task
def extract_chains_from_pdb(input_file_name: str, chains_lookup_list: list[str]):
    file_path = Path(INPUT_FOLDER_NAME) / input_file_name
    file_provider = LocalFileProvider(file_path)
    chains_data = PDBFileProcessor(file_provider).find_atom_chains_from_list(
        chains_lookup_list
    )
    output_filename = FileExporter(input_file_name, OUTPUT_DIRECTORY_NAME).write_output_file(
        chains_data
    )
    return output_filename


@app.task
def run_model_on_chains(chain_output_file_name: str):
    output_file_path = Path(OUTPUT_DIRECTORY_NAME) / chain_output_file_name
    chains_iterator = GetChainsFromFile(output_file_path).get_chains_iterator()
    for chain in chains_iterator:
        prediction_results = T5ModelExecutor().process_sequence(chain)
        PredictionFileExporter(chain, OUTPUT_DIRECTORY_NAME).export_prediction_results(
            prediction_results
        )
