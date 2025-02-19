import pprint

from pdb_file_processor import PDBFileProcessor


def main():
    file_name = "1bey.pdb"
    procesor = PDBFileProcessor(file_name)
    pprint.pprint(procesor.find_atom_chains_from_list(["H", "L"]))


if __name__ == "__main__":
    main()
