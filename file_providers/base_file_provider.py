import abc
from typing import Iterator


class BaseFileProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_atom_rows_iterator(self) -> Iterator:
        pass

    @property
    @abc.abstractmethod
    def file_name(self) -> str:
        pass
