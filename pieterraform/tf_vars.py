import hcl2
import pathlib
from typing import List


class Var:
    def __init__(self, name, default, description):
        self.name: str = name
        self.default = default
        self.description: str = description


class TfVars:
    def __init__(self, tf_folder: str):
        self.current = -1
        self._vars: Dict[str, TfVar] = {}
        variable_key = "variable"
        description_key = "description"
        default_key = "default"
        for tf in pathlib.Path(tf_folder).glob("*.tf"):
            with tf.open("r") as f:
                try:
                    data = hcl2.load(f)
                except Exception as e:
                    continue
                if not data or variable_key not in data:
                    continue
                try:
                    _ = (e for e in data[variable_key])
                except TypeError as e:
                    continue
                for r in data[variable_key]:
                    for k, v in r.items():
                        var_name = k
                        var_help = ""
                        var_default = None
                        if description_key in v:
                            var_help = v[description_key][0]
                        if default_key in v:
                            var_default = v[default_key][0]
                        self._vars[var_name] = Var(var_name, var_default, var_help)

    @property
    def vars(self):
        return self._vars

    def __iter__(self):
        return iter(self._vars.keys())

    def __getitem__(self, key):
        return self._vars.__getitem__(key)
