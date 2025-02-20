from typing import Iterator
from file_providers.base_file_provider import BaseFileProvider

from pathlib import Path


class LocalFileProvider(BaseFileProvider):
    ATOM_ROW_PREFIX = "ATOM"

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)

    def get_atom_rows_iterator(self) -> Iterator:
        with open(self.file_path, "r") as pdb_file:
            for row in pdb_file:
                if row.startswith(self.ATOM_ROW_PREFIX):
                    yield row.split()

    @property
    def file_name(self) -> str:
        return self.file_path.name
