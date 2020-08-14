import logging
import subprocess
from typing import List


def run_it(command: List[str],
           logger: logging.Logger = None,
           work_dir: str = '.') -> List[str]:
    outputs = []
    if logger is not None:
        logger.debug(command)
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               universal_newlines=True,
                               cwd=work_dir)
    while True:
        output = process.stdout.readline().strip()
        if output == '' and process.poll() is not None:
            break
        if not output:
            continue
        outputs.append(output)
        if logger is None:
            continue
        f = __get_logger_type(output, logger)
        f(output)
    rc = process.poll()
    if rc == 0:
        return outputs
    else:
        raise subprocess.CalledProcessError(rc, command, outputs)


def __get_logger_type(output: str, logger: logging.Logger):
    if 'error' in output.lower():
        return logger.error
    if 'warn' in output.lower():
        return logger.warn
    return logger.info
