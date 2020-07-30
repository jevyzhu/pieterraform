from .cmd_runner_base import CmdRunnerBase

class OptsBase:
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
    def options(self): return self._options

class TfCommonOpts(OptsBase):
    def __init__(self):
        super().__init__()

    @OptsBase.option('-no-color')
    def no_color(self): return self