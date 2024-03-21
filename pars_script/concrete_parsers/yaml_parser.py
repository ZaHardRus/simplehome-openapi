import json
from typing import Dict, List
import yaml
from pars_script import Parser
from pars_script.exceptions import ParserException


class YamlParser(Parser):

    file_format = "yaml"

    @staticmethod
    def read_file(file_path: str):
        with open(file_path, "r") as file:
            return yaml.load(file, Loader=yaml.CSafeLoader)

    @classmethod
    def parse(cls, file_path: str):
        print("run yaml parser")
        yaml_obj: dict = cls.read_file(file_path=file_path)
        paths: dict = yaml_obj.get("paths")
        if paths is None:
            raise ParserException("Fail to get 'paths' from file")

        components: Dict[str, dict] = {
            "parameters": {},
            "schemas": {},
            "headers": {},
            "securitySchemes": {},
            "requestBodies": {},
            "responses": {},
            "headers": {},
            "examples": {},
            "links": {},
            "callbacks": {}
        }
        
        requests: Dict[str, dict]
        for requests in paths.values():
            if requests.get("components") is None:
                continue
            for subsection_name in components.keys():
                components[subsection_name].update(requests["components"].get(subsection_name, {}))
            requests.pop("components")
        yaml_obj["components"] = {k:v for k, v in components.items() if v != {}}
        print(json.dumps(yaml_obj, indent=4))
        
