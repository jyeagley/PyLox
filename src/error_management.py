
import logging

logger = logging.getLogger("PyLox")
had_error = False


def error(line, message):
    report(line, "", message)
# -----------------------------------------------------------------------------


def report(line, where, message):
    logger.error(f"{where} line {line}: {message}")
    global had_error
    had_error = True
# -----------------------------------------------------------------------------