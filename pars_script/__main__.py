import sys
from typing import Any, Dict

from pars_script import Parser
from pars_script.concrete_parsers.yaml_parser import YamlParser

def run():
    parser_params = get_shell_arguments()
    Parser.run_parser(**parser_params)


def get_shell_arguments():
    parser_params: Dict[str, Any] = {}
    shell_args = sys.argv
    for arg_index in range(len(shell_args[1:])):  # first element is file path
        arg = shell_args[arg_index]
        if arg not in Parser.parser_arguments_map:
            continue
        argument_properties = Parser.parser_arguments_map[arg]
        arg_name: str = argument_properties["name"]
        arg_type: type = argument_properties["type"]
        try:
            arg_value = shell_args[arg_index+1]
        except IndexError:
            break
        parser_params[arg_name] = arg_type(arg_value)
    return parser_params
    

if __name__ == "__main__":
    run()
