# tests: lint, mypy

import time
import codecs
import sys
import os

# pylint: disable=unused-import
from typing import Any, Optional
from termcolor import colored


class Logging(object):

    log_file = None  # type: Optional[Any]

    # 'all' and 'none' are special symbols,
    # others are filtered according the labels
    debug_enabled = [
        os.environ.get("NEURALMONKEY_DEBUG_ENABLE", "none")]  # type: List[str]
    debug_disabled = [
        os.environ.get("NEURALMONKEY_DEBUG_DISABLE", "")]  # type: List[str]

    @staticmethod
    def set_log_file(path):
        """Sets up the file where the logging will be done."""
        Logging.log_file = codecs.open(path, 'w', 'utf-8', buffering=0)

    @staticmethod
    def log_print(text: str) -> None:
        """Prints a string both to console and
        a log file is it is defined.
        """
        if Logging.log_file is not None:
            if not isinstance(text, str):
                text = str(text)
            Logging.log_file.write(text + "\n")
            Logging.log_file.flush()

        print(text, file=sys.stderr)

    @staticmethod
    def log(message, color='yellow'):
        """Logs message with a colored timestamp."""
        log_print("{}: {}".format(colored(
            time.strftime("%Y-%m-%d %H:%M:%S"), color), message))

    @staticmethod
    def warning(message):
        """Logs a warning."""
        log_print(colored("{}: Warning! {}".format(
            time.strftime("%Y-%m-%d %H:%M:%S"), message), color='red'))

    @staticmethod
    def print_header(title):
        """Prints the title of the experiment and
        the set of arguments it uses.
        """
        log_print(colored("".join("=" for _ in range(80)), 'green'))
        log_print(colored(title.upper(), 'green'))
        log_print(colored("".join("=" for _ in range(80)), 'green'))
        log_print("Launched at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

        log_print("")

    @staticmethod
    def debug(message, label=None):
        if 'none' in Logging.debug_enabled:
            return

        if (label not in Logging.debug_enabled and
                'all' not in Logging.debug_enabled):
            return

        if label in Logging.debug_disabled:
            return

        if label:
            prefix = "DEBUG ({}):".format(label)
        else:
            prefix = "DEBUG:"

        log_print("{}{}".format(colored(prefix, color="cyan"), message))


# pylint: disable=invalid-name
# we want these helper functions to have this exact name
log = Logging.log
log_print = Logging.log_print
debug = Logging.debug
warning = Logging.warning
