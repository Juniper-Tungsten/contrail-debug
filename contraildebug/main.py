import sys
from utils.argparser import parse_args
from utils.logger import setup_logger


args = parse_args(sys.argv)
log_file = gen_log_filename()
log = setup_logger(log_file)
