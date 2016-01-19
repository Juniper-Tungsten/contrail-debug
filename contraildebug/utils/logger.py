import logging


def setup_logger(log_file):
    """Root logger for the contraildebug.
    """
    log = logging.getLogger('contraildebug')
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '[%(asctime)s %(module)s(%(lineno)s) %(levelname)s]: %(message)s',
        datefmt='%a %b %d %H:%M:%S %Y', fsecs="%.9f")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    return log
