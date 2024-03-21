from abc import ABC, abstractmethod
from typing import Optional

from pars_script.exceptions import ParserException


class Parser(ABC):

    parser_arguments_map = {
        "--file": {"name": "file_path", "type": str},
        "--format": {"name": "file_format", "type": str}
    }
    file_format: str

    @classmethod
    @abstractmethod
    def parse(cls, file_path: str):
        ...

    @staticmethod
    @abstractmethod
    def read_file(file_path: str):
        ...

    @classmethod
    def run_parser(cls, file_path: str, file_format: Optional[str] = None):
        if file_format is None:
            try:
                file_format = file_path.split(".")[-1].rstrip()
            except IndexError:
                print("Fail to get file format")
                return
        print(cls.__subclasses__())
        for subclass in cls.__subclasses__():
            if subclass.__dict__.get("file_format") == file_format:
                try:
                    subclass.parse(file_path)
                except ParserException as ex:
                    print("Failure:", ex)
                return
        print("Fail to find parser for", file_format, "file format")
