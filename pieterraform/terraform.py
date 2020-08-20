import logging
import shutil
from .context import CmdContext
from .runner_base import CmdRunnerBase



class Terraform(CmdContext):
    def __default_logger():
        logFormatter = logging.Formatter('%(message)s')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        c_handler = logging.StreamHandler()
        c_handler.setFormatter(logFormatter)
        c_handler.setLevel(logging.DEBUG)
        logger.addHandler(c_handler)
        return logger

    def __init__(self,
                 tf_exec_path: str = 'terraform',
                 logger: logging = __default_logger()):
        tf_exec = shutil.which(tf_exec_path)
        if tf_exec:
            self._tf_exec = tf_exec_path
        else:
            raise FileNotFoundError(f'Cannot find {tf_exec_path}')
        super().__init__([self._tf_exec], '.')
        self._logger = logger

    def version(self):
        return TfVersion(self, self._logger)

    def init(self):
        return TfInit(self, self._logger)

    def plan(self):
        return TfPlan(self, self._logger)

    def apply(self):
        return TfApply(self, self._logger)

    def destroy(self):
        return TfDestroy(self, self._logger)


# To avoid circle ref
from .level1 import TfInit, TfPlan, TfApply, TfDestroy, TfVersion
