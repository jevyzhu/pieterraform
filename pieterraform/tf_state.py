import json
import pathlib


class TfState:
    class Object(object):
        pass

    def __init__(self, state_file_path: str):
        self.output = TfState.Object()
        with open(state_file_path, "r") as f:
            outputs = json.load(f)['outputs']
            for key in outputs:
                value = outputs[key]['value']
                setattr(self.output, key, value)
