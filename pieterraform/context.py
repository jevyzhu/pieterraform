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
        self._results: List[RunHistory] = []
        self._fake_run = False

    def workdir(self, value: str):
        self._work_dir = value
        return self

    @property
    def cmd(self):
        return self._cmd

    @property
    def results(self) -> List[RunHistory]:
        return self._results

    @property
    def last_result(self) -> RunHistory:
        if len(self.results) > 0:
            return self.results[-1]
        return None

    def fake_run(self):
        self._fake_run = True
        return self

    def real_run(self):
        self._fake_run = False
        return self

    def clean_result(self):
        self.results.clear()
