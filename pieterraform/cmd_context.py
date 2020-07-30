from typing import List, Tuple


class RunHistory:
    def __init__(self, command: List[str], output: List[str]):
        self.command = command
        self.output = output


class CmdContext:
    def __init__(self, cmd: List, work_dir: str):
        self._cmd = cmd
        self._work_dir = work_dir
        self._last_run = None
        self._run_history: List[RunHistory] = []
        self._fake_run = False

    def workdir(self, value: str):
        self._work_dir = value
        return self

    @property
    def cmd(self):
        return self._cmd

    @property
    def run_history(self) -> List[RunHistory]:
        return self._run_history

    @property
    def last_run(self) -> RunHistory:
        if len(self._run_history) > 0:
            return self._run_history[-1]
        return None

    def fake_run(self):
        self._fake_run = True
        return self

    def real_run(self):
        self._fake_run = False
        return self
