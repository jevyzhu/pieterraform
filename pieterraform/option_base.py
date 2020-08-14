class OptionBase:
    def __init__(self):
        self._options = []

    def option(opt: str):
        def wrap(func):
            def wrapper(self, *args, **kwargs):
                self._options.append(opt)
                func(self, *args, **kwargs)
                return self

            return wrapper

        return wrap

    @property
    def options(self):
        return self._options


class TfCommonOpts(OptionBase):
    def __init__(self):
        super().__init__()

    @OptionBase.option('-no-color')
    def no_color(self):
        return self
