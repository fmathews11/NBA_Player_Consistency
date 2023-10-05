import logging
from typing import Literal
import sys

type_conversion_dict = {'debug': logging.DEBUG,
                        'error': logging.ERROR,
                        'critical': logging.CRITICAL,
                        'info': logging.INFO,
                        'warning': logging.WARNING}

allowed_logging_values = Literal['debug', 'error', 'critical', 'info', 'warning']


def create_logger(logger_name: str,
                  logging_level: allowed_logging_values) -> logging.Logger:
    """Returns a logging.Logger object with the name assigned to the `logger_name` parameter
    and the logging level assigned to the `logging_level` parameter

    Parameters:
    -----------
        - logger_name: str
            The name of the logger.  Equivalent to `logging.getLogger(<NAME HERE>)
        - logging_level: Literal['debug', 'error', 'critical', 'info', 'warning']
            The level of logging to log

    Returns:
    -----------
        - A logger.Logging object with the provided name and logging level
    """
    # Input validation
    if logging_level not in ['debug', 'error', 'critical', 'info', 'warning']:
        raise AttributeError(
            "Argument passed to `logging_level` must be one of"
            " ['debug','error','critical','info','warning']"
        )

    # Determine whether we are in an interactive environment
    interactive = False
    try:
        # This is only defined in interactive shells
        if sys.ps1:
            interactive = True
    except AttributeError:
        interactive = sys.flags.interactive

    logger = logging.getLogger(logger_name)

    # If we are in an interactive environment (like jupyter), set loglevel to info
    # and pipe the output to stdout
    if interactive:
        logger.setLevel(type_conversion_dict.get(logging_level))
        logging_target = sys.stdout
    else:
        logging_target = sys.stderr

    # Add the output handler
    if not logger.handlers:
        handler = logging.StreamHandler(logging_target)
        handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT, None))
        logger.addHandler(handler)
    # Disable propagation and return
    logger.propagate = False
    return logger

if __name__ == '__main__':
    test_logger = create_logger('test_logger',logging_level='debug')
    print(test_logger.debug("HELLO"))
