#!/usr/bin/python3
# coding=utf-8
import sys
import os
import logging
import atexit
import argparse


# Main function. This function serves as the starting point for program execution.
def main(command_line_arguments) -> int:
    logger.debug("Main")

    if command_line_arguments.script:
        print(f"Executing Lox script \"{command_line_arguments.script}\"")
    else:
        print("Entering Lox interpreter mode!")

    return EXIT_SUCCESS
# -----------------------------------------------------------------------------


# This block seves as the program entrypoint similar to _libc_start_main in c. It does some
# basic environmental handling then passes execution to main().
if __name__ == "__main__":

    global EXIT_SUCCESS
    EXIT_SUCCESS = 0
    global EXIT_FAILURE
    EXIT_FAILURE = 1
    global MODULE_NAME
    MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
    global LOG_PATH
    LOG_PATH = "./logs"
    global LOG_FILE
    LOG_FILE = MODULE_NAME + ".log"

    # Function called when module exits. This can be used to clean up if necessary.
    def module_cleanup():
        logger.debug("Module \"{}\" exiting, Goodbye!".format(MODULE_NAME))
        logging.shutdown()  # Flush the log and close out the file
    # -------------------------------------------------------------------------

    # Should be the first thing called. it sets up the root logger
    # returns the module logger instance
    def setup_logger(log_level, log_path=LOG_PATH, log_file=LOG_FILE, remove_preexisting=False):
        if remove_preexisting:
            # Remove all prexisting handlers associated with the root logger object.
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
        lgr = logging.getLogger(__name__)
        lgr.setLevel(log_level)
        return lgr
    # -------------------------------------------------------------------------

    cla_parser = argparse.ArgumentParser()
    cla_parser.add_argument("script", nargs='?', help="filename of a Lox script to execute")
    try:
        global logger
        logger = setup_logger(logging.INFO)
        atexit.register(module_cleanup)
        exit_code: int = main(cla_parser.parse_args())
        if exit_code is not None:
            sys.exit(exit_code)
        else:
            sys.exit(EXIT_SUCCESS)
    except Exception as e:
        import traceback

        logging.error("Exception caught at entrypoint! Message=\"{}\". Traceback:\n{}".format(e, ''.join(
            traceback.format_tb(e.__traceback__))))
        sys.exit(EXIT_FAILURE)
# -----------------------------------------------------------------------------
