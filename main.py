from pdb_processors.pdb_custom_processor import PDBFileProcessor
from file_providers.local_file_provider import LocalFileProvider
from pdb_processors.pdb_biopython_processor import parse_pdb_file


def main():
    file_name = "1bey.pdb"
    file_provider = LocalFileProvider(file_name)
    procesor = PDBFileProcessor(file_provider)
    chains_map = procesor.find_atom_chains_from_list(["H", "L"])
    for chain_id, residue in chains_map.items():
        print(f"Chain_{chain_id}: {''.join(residue)}")
    print("-------------------------------------------")
    parse_pdb_file(file_name)


if __name__ == "__main__":
    main()
