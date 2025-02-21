from exporters.chain_file_exporter import FileExporter
from file_providers.local_file_provider import LocalFileProvider
from pdb_processors.pdb_biopython_processor import parse_pdb_file
from pdb_processors.pdb_custom_processor import PDBFileProcessor


def main():
    file_name = "1bey.pdb"
    file_provider = LocalFileProvider(file_name)
    procesor = PDBFileProcessor(file_provider)
    chains_map = procesor.find_atom_chains_from_list(["H", "L"])
    exporter = FileExporter(file_name)
    exporter.write_output_file(chains_map)


if __name__ == "__main__":
    main()
