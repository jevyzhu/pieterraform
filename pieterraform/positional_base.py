class PositionalBase:
    def __init__(self):
        self._positionals = []

    def positional(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._positionals.append(result)
            return self

        return wrapper

    @property
    def positionargs(self):
        return self._positionals
