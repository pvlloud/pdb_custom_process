from collections import OrderedDict

from Bio import PDB

from utils import get_mapping_dict_from_file


def extract_unique_residues(pdb_file: str):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("PDB_structure", pdb_file)
    chain_residues = {}
    for model in structure:
        for chain in model:
            chain_id = chain.id
            if chain_id not in chain_residues:
                chain_residues[chain_id] = OrderedDict()
            for residue in chain:
                if PDB.is_aa(residue, standard=True):
                    res_seq = residue.id[1]
                    res_name = residue.get_resname()
                    if res_seq not in chain_residues[chain_id]:
                        chain_residues[chain_id][res_seq] = res_name
    return chain_residues


def parse_pdb_file(file_path: str):
    ordered_residues = extract_unique_residues(file_path)
    three_to_one = get_mapping_dict_from_file("mapping.json")

    for chain, residues in ordered_residues.items():
        three_to_one_seq = "".join(
            [
                three_to_one[res.title().upper()]
                for res in residues.values()
                if res.title().upper() in three_to_one
            ]
        )
        ordered_residues[chain] = three_to_one_seq
        return ordered_residues
