#!/usr/bin/env python
import logging
from config_helper import read_config_map


def init():
    """
    this function handles global variables
    initialization.
    :return:
    """
    global amount
    global logger
    amount = [0]

    # define logger
    file_name = read_config_map("runtime_globals")["log_file"]
    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler(file_name[1:-1])
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
