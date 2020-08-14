from typing import List, Tuple


class ArgumentBase:
    def __init__(self):
        self._arguments: List[Tuple[str, str]] = []

    def param(param: str):
        def wrap(func):
            def wrapper(self, *args, **kwargs):
                result = func(self, *args, **kwargs)
                if param:
                    self._arguments.append((param, result))
                else:
                    self._arguments.append((result))
                return self

            return wrapper

        return wrap

    @property
    def arguments(self):
        value = []
        for v in self._arguments:
            value.extend(v)
        return value
