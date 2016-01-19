import os
import datetime
import logging


LOG_DIR = os.path.expanduser('~/contraildebug/logs/')


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
        datefmt='%a %b %d %H:%M:%S %Y')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    return log


def gen_log_filename(sub_name):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    ts = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    return '%s/contraildebug-%s-%s.log' % (LOG_DIR, sub_name, ts)
