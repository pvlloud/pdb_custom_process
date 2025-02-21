from typing import Iterable, List, Set

from exceptions import MissingAtomsException
from file_providers.base_file_provider import BaseFileProvider
from utils import get_mapping_dict_from_file

AMINO_MAPPING_FILE_PATH = "mapping.json"


class PDBFileProcessor:
    COLUMN_MAP = {
        "spec": 0,
        "index": 1,
        "element": 2,
        "amino_acid": 3,
        "chain": 4,
        "sequence_number": 5,
        "coordinate_x": 6,
        "coordinate_y": 7,
        "coordinate_z": 8,
    }

    required_atoms = ["C", "CA", "O", "N"]

    def __init__(self, file_provider: BaseFileProvider) -> None:
        self.file_provider = file_provider

    def _get_all_atoms_from_lines(self, atom_lines: Iterable) -> Set[str]:
        element_column_index = self.COLUMN_MAP["element"]
        return {line[element_column_index] for line in atom_lines}

    def validate_atom_lines(self):
        distinct_atoms_set = self.file_provider.get_atom_rows_iterator()
        for check_atom in self.required_atoms:
            if check_atom not in distinct_atoms_set:
                raise MissingAtomsException(
                    f"Atom {check_atom} not found in {self.file_provider.file_name} file"
                )

    @staticmethod
    def _get_amino_one_letter_code(amino_acid: str) -> str:
        amino_codes_mapping = get_mapping_dict_from_file("mapping.json")
        return amino_codes_mapping[amino_acid]

    @staticmethod
    def _add_amino_if_not_as_last(aminos_chain: List[str], new_amino: str):
        if not aminos_chain:
            aminos_chain.append(new_amino)
        elif aminos_chain[-1] != new_amino:
            aminos_chain.append(new_amino)

    def find_atom_chains_from_list(self, chains_lookup: list):
        atom_lines = self.file_provider.get_atom_rows_iterator()
        chain_column_index = self.COLUMN_MAP["chain"]
        amino_column_index = self.COLUMN_MAP["amino_acid"]
        chain_amino_mapping = {chain: list() for chain in chains_lookup}
        for line in atom_lines:
            if (line_chain := line[chain_column_index]) in chains_lookup:
                amino_code = line[amino_column_index]
                amino_one_letter = self._get_amino_one_letter_code(amino_code)
                self._add_amino_if_not_as_last(
                    chain_amino_mapping[line_chain], amino_one_letter
                )
        return chain_amino_mapping
