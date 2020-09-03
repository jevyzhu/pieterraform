import json
import pathlib
from argparse import Namespace


class TfState:
    def __init__(self, state_file_path: str):
        self.output = Namespace()
        with open(state_file_path, "r") as f:
            outputs = json.load(f)["outputs"]
            for key in outputs:
                value = outputs[key]["value"]
                setattr(self.output, key, value)
