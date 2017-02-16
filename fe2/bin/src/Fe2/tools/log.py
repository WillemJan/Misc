# -*- coding: utf-8 -*-
"""
    Implements the logging support for Fe2.
"""

import os
import sys
import logging


def create_logger(app):
    log = Log(app)
    return(log.create_logger())


class Log():
    """
        Basic logging implementation.

        >>> log = Log(app)
        >>> log = log.create_logger()
        >>> log.info("test")
        ...
    """
    def __init__(self, app):
        self.app = app
        pass

    def create_logger(self):
        """
            Creates a logger for the application.

            >>> log = create_logger("test")
            >>> log.info("Warning")
        """
        logging.basicConfig()
        logger = logging.getLogger(self.app)
        logger.setLevel(logging.DEBUG)
        return(logger)

    if __name__ == "__main__":
        main(sys.argv)
