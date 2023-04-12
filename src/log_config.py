import logging
import os
import sys

# Globals
LOG_PATH = "./logs"
MODULE_NAME = "PyLox"
LOG_FILE = MODULE_NAME + ".log"


# Should be the first thing called. it sets up the root logger
# returns the module logger instance
def setup_logger(log_level, log_path=LOG_PATH, log_file=LOG_FILE, remove_preexisting=False):
    if remove_preexisting:
        # Remove all preexisting handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s {:<20s} [%(levelname)-5s] %(message)s".format(MODULE_NAME),
        handlers=[
            logging.FileHandler("{}/{}".format(log_path, log_file), mode="w", delay=True),
            logging.StreamHandler(sys.stdout)
        ]
    )
    lgr = logging.getLogger(MODULE_NAME)
    lgr.setLevel(log_level)
    return lgr
# -------------------------------------------------------------------------
