import sys
from utils.argsparser import parse_args
from utils.logger import setup_logger, gen_log_filename


args = parse_args(sys.argv[1:])
log_file = gen_log_filename(sys.argv[1])
log = setup_logger(log_file)


def main():
    prefix = 'contraildebug.scripts'
    module = __import__('%s.%s' % (prefix, sys.argv[1]), fromlist='_')
    module.main(args)


if __name__ == '__main__':
    sys.exit(main())
