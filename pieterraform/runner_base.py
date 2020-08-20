from typing import List
from abc import ABC, abstractproperty
import logging
from .runit import run_it
from .context import CmdContext, RunHistory


class CmdRunnerBase(ABC):
    def __init__(self,
                 context: CmdContext,
                 cmd: str = '',
                 logger: logging = None):
        self._context = context
        self._sub_cmd = cmd
        self._logger = logger

    def run(self):
        cmd = self._context.cmd  \
            + [self._sub_cmd]  \
            + self.all_arguments
        output = None
        if not self._context._fake_run:
            output = run_it(cmd,
                            self._logger,
                            work_dir=self._context._work_dir)
        self._context.results.append(RunHistory(cmd, output))
        return self._context

    @property
    def all_arguments(self) -> List:
        options = self.options if hasattr(self, 'options') else []
        arguments = self.arguments if hasattr(self, 'arguments') else []
        positions = self.positionargs if hasattr(self, 'positionargs') else []
        return options + arguments + positions
