#!/usr/bin/python3
# coding=utf-8
import sys
import os
import logging
import atexit
import argparse
from token import Token, TokenType
from log_config import setup_logger
from error_management import error, report, had_error


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    # For now, just print the tokens.
    for token in tokens:
        print(token)
# -----------------------------------------------------------------------------


def run_file(filename):
    with open(filename, 'rb') as file:
        bytes = file.read()
        run(bytes.decode())
    pass
# -----------------------------------------------------------------------------


def run_prompt():
    while True:
        try:
            line = input("> ")
            if not line:
                break
            run(line)
        except EOFError:
            break
# -----------------------------------------------------------------------------


# Main function. This function serves as the starting point for program execution.
def main(command_line_arguments) -> int:
    logger.debug("Main")

    if command_line_arguments.script:
        print(f"Executing Lox script \"{command_line_arguments.script}\"")
        run_file(command_line_arguments.script)
    else:
        print("Entering Lox interpreter mode!")
        run_prompt()

    return EXIT_SUCCESS if not had_error else EXIT_FAILURE
# -----------------------------------------------------------------------------


# This block seves as the program entrypoint similar to _libc_start_main in c. It does some
# basic environmental handling then passes execution to main().
if __name__ == "__main__":

    global EXIT_SUCCESS
    EXIT_SUCCESS = 0
    global EXIT_FAILURE
    EXIT_FAILURE = 1
    global MODULE_NAME

    # Function called when module exits. This can be used to clean up if necessary.
    def module_cleanup():
        logger.debug("Module \"{}\" exiting, Goodbye!".format(MODULE_NAME))
        logging.shutdown()  # Flush the log and close out the file
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
