import datetime
import json
import re
from typing import Any, Dict
import yaml
from pars_script import Parser
from pars_script.exceptions import ParserException


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class YamlParser(Parser):

    file_format = "yaml"

    @staticmethod
    def read_file(input_file_path: str):
        with open(input_file_path, "r") as file:
            return yaml.load(file, Loader=yaml.CSafeLoader)

    @staticmethod
    def write_file(input_file_path: str, data: Any):
        with open(input_file_path, "w") as file:
            yaml.dump(data=data,
                      stream=file,
                      Dumper=yaml.CSafeDumper,
                      allow_unicode=True)

    @classmethod
    def parse(cls, input_file_path: str):
        print("run yaml parser")
        yaml_obj: dict = cls.read_file(input_file_path=input_file_path)
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
        for path, requests in paths.items():
            if requests.get("components") is None:
                continue
            for subsection_name in components.keys():
                components[subsection_name].update(requests["components"].get(subsection_name, {}))
            paths[path].pop("components")
        paths = cls.__update_references(paths)
        components = {k:v for k, v in components.items() if v != {}}
        yaml_obj["components"] = components
        cls.write_file(input_file_path="dump_file.yaml", data=yaml_obj)
        with open("json_dump_file.json", "w") as file:
            json.dump(yaml_obj, file, indent=1, cls=CustomEncoder)

    @classmethod
    def __update_references(cls, paths: dict) -> dict:
        def __update_ref(value):
            if isinstance(value, str) and name == "$ref":
                components_index = value.find("components")
                if components_index == -1:
                    return
                value = f"#/{value[components_index:]}"
                paths[name] = value

        for name, value in paths.items():
            if isinstance(value, dict):
                cls.__update_references(value)
            if isinstance(value, list):
                for vid in range(len(value)):
                    if isinstance(value[vid], dict):
                        value[vid] = cls.__update_references(value[vid])
                    else:
                        __update_ref(value)
            else:
                __update_ref(value)           
        return paths
