import pprint


def read_atom_rows_from_file(file_path):
    with open(file_path, "r") as pdb_file:
        for row in pdb_file:
            if row.startswith("ATOM"):
                yield row.split()


def main():
    atom_lines = read_atom_rows_from_file("1bey.pdb")
    for line in atom_lines:
        pprint.pprint(line)


if __name__ == "__main__":
    main()
