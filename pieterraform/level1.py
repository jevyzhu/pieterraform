from typing import List
import logging
from .runner_base import CmdRunnerBase
from .terraform import Terraform
from .argument_base import ArgumentBase
from .positional_base import PositionalBase
from .common_options import TfCommonOpts
from .option_base import OptionBase


class TfCmdRunner(CmdRunnerBase):
    def run(self) -> Terraform:
        return super().run()


class TfVersion(TfCmdRunner, TfCommonOpts):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, 'version', logger)
        TfCommonOpts.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options


class TfInit(TfCmdRunner, TfCommonOpts):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, 'init', logger)
        TfCommonOpts.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options

    @OptionBase.option('-upgrade=false')
    def no_upgrade(self):
        pass


class TfPlan(TfCmdRunner, TfCommonOpts, ArgumentBase):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, 'plan', logger)
        TfCommonOpts.__init__(self)
        ArgumentBase.__init__(self)
        self._var_param_str = None

    @OptionBase.option('-destroy')
    def destroy(self):
        pass

    @ArgumentBase.param('-var')
    def var(self, k: str, v: str):
        return f'{k}={v}'

    @ArgumentBase.param('-out')
    def out(self, value: str):
        return value

    @ArgumentBase.param('-state')
    def statefile(self, value: str):
        return value

    @property
    def all_arguments(self) -> List:
        return self.options + self.arguments


class TfApply(TfCmdRunner, TfCommonOpts, ArgumentBase, PositionalBase):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, 'apply', logger)
        TfCommonOpts.__init__(self)
        ArgumentBase.__init__(self)
        PositionalBase.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options + self.arguments + self.positionargs

    @PositionalBase.positional
    def use_plan(self, value: str):
        return value

    @ArgumentBase.param('-state')
    def statefile(self, value: str):
        return value


class TfDestroy(TfCmdRunner, TfCommonOpts, ArgumentBase):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, 'destroy', logger)
        TfCommonOpts.__init__(self)
        ArgumentBase.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options + self.arguments

    @OptionBase.option('-auto-approve')
    def auto_approve(self):
        pass

    @ArgumentBase.param('-state')
    def statefile(self, value: str):
        return value
