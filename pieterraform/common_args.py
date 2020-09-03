from .option_base import OptionBase
from .positional_base import PositionalBase
from .argument_base import ArgumentBase


class TfCommonArgs(OptionBase, PositionalBase):
    def __init__(self):
        OptionBase.__init__(self)
        PositionalBase.__init__(self)

    @OptionBase.option("-no-color")
    def no_color(self):
        return self

    @PositionalBase.positional
    def dir(self, value: str):
        return value


class TfVarArgs(TfCommonArgs, ArgumentBase):
    def __init__(self):
        TfCommonArgs.__init__(self)
        ArgumentBase.__init__(self)

    @ArgumentBase.param("-var")
    def var(self, k: str, v: str):
        return f"{k}={v}"
