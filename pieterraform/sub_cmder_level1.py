from typing import List
import logging
from .cmd_runner_base import CmdRunnerBase
from .tf_cmder import Terraform
from .arguments import ArgsBase
from .options import OptsBase, TfCommonOpts


class Tf1stCmdRunner(CmdRunnerBase):
    def run(self) -> Terraform: return super().run()


class TfVersion(Tf1stCmdRunner, TfCommonOpts):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        Tf1stCmdRunner.__init__(self, parent_cmder, 'version', logger)
        TfCommonOpts.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options


class TfInit(Tf1stCmdRunner, TfCommonOpts):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        Tf1stCmdRunner.__init__(self, parent_cmder, 'init', logger)
        TfCommonOpts.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options

    @OptsBase.option('-upgrade=false')
    def no_upgrade(self): pass


class TfPlan(Tf1stCmdRunner, TfCommonOpts, ArgsBase):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        Tf1stCmdRunner.__init__(self, parent_cmder, 'plan', logger)
        TfCommonOpts.__init__(self)
        ArgsBase.__init__(self)
        self._var_param_str = None

    @OptsBase.option('-destroy')
    def destroy(self): pass

    @ArgsBase.param('-var')
    def var(self, k: str, v: str):
        return f'{k}={v}'

    @ArgsBase.param('-out')
    def out(self, value: str):
        return value

    @ArgsBase.param('-state')
    def statefile(self, value: str):
        return value

    @property
    def all_arguments(self) -> List:
        return self.options + self.arguments


class TfApply(Tf1stCmdRunner, TfCommonOpts, ArgsBase):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        Tf1stCmdRunner.__init__(self, parent_cmder, 'apply', logger)
        TfCommonOpts.__init__(self)
        ArgsBase.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options + self.arguments

    @ArgsBase.param('')
    def use(self, value: str):
        return value


class TfDestroy(Tf1stCmdRunner, TfCommonOpts, ArgsBase):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        Tf1stCmdRunner.__init__(self, parent_cmder, 'destroy', logger)
        TfCommonOpts.__init__(self)
        ArgsBase.__init__(self)

    @property
    def all_arguments(self) -> List:
        return self.options + self.arguments

    @OptsBase.option('-auto-approve')
    def auto_approve(self): pass
