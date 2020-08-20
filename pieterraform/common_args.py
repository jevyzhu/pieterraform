from .option_base import OptionBase
from .positional_base import PositionalBase


class TfCommonArgs(OptionBase, PositionalBase):
    def __init__(self):
        OptionBase.__init__(self)
        PositionalBase.__init__(self)

    @OptionBase.option('-no-color')
    def no_color(self):
        return self

    @PositionalBase.positional
    def dir(self, value: str):
        return value
