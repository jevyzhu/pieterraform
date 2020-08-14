from .option_base import OptionBase


class TfCommonOpts(OptionBase):
    def __init__(self):
        super().__init__()

    @OptionBase.option('-no-color')
    def no_color(self):
        return self
