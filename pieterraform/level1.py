from typing import List
import logging
from .runner_base import CmdRunnerBase
from .terraform import Terraform
from .argument_base import ArgumentBase
from .positional_base import PositionalBase
from .common_args import TfCommonArgs, TfVarArgs
from .option_base import OptionBase


class TfCmdRunner(CmdRunnerBase):
    def run(self) -> Terraform:
        return super().run()


class TfVersion(TfCmdRunner):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, "version", logger)


class TfInit(TfCmdRunner, ArgumentBase, TfCommonArgs):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, "init", logger)
        ArgumentBase.__init__(self)
        TfCommonArgs.__init__(self)

    @OptionBase.option("-upgrade=false")
    def no_upgrade(self):
        pass

    @OptionBase.option("--reconfigure=true")
    def reconfigure(self):
        pass

    @ArgumentBase.param("-backend-config")
    def backend_config(self, value: str):
        return value


class TfPlan(TfCmdRunner, TfVarArgs):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, "plan", logger)
        TfVarArgs.__init__(self)

    @OptionBase.option("-destroy")
    def destroy(self):
        pass

    @ArgumentBase.param("-out")
    def out(self, value: str):
        return value

    @ArgumentBase.param("-state")
    def statefile(self, value: str):
        return value


class TfApply(TfCmdRunner, TfVarArgs):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, "apply", logger)
        TfVarArgs.__init__(self)

    @PositionalBase.positional
    def use_plan(self, value: str):
        return value

    @ArgumentBase.param("-state")
    def statefile(self, value: str):
        return value


class TfDestroy(TfCmdRunner, TfVarArgs):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, "destroy", logger)
        TfVarArgs.__init__(self)

    @OptionBase.option("-auto-approve")
    def auto_approve(self):
        pass

    @ArgumentBase.param("-state")
    def statefile(self, value: str):
        return value


class TfOutput(TfCmdRunner, TfCommonArgs):
    def __init__(self, parent_cmder: Terraform, logger: logging = None):
        TfCmdRunner.__init__(self, parent_cmder, "output", logger)
        TfCommonArgs.__init__(self)

    @ArgumentBase.param("-state")
    def statefile(self, value: str):
        return value

    @OptionBase.option("-json=True")
    def json(self):
        pass
