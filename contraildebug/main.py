import sys
from utils.argsparser import parse_args
from utils.logger import setup_logger, gen_log_filename

# fabric requires paramiko, which in turn require threading, so patching
# the threading module as well which is skipped in (https://github.com/Juniper/
# contrail-sandesh/blob/master/library/python/pysandesh/sandesh_http.py#L19)
# Without the patch in threading, due to incompatability between unpatched
# threading and patched other modules, ssh dosent go through.
from gevent import monkey
monkey.patch_thread()

args = parse_args(sys.argv[1:])
log_file = gen_log_filename(sys.argv[1])
log = setup_logger(log_file)


def main():
    prefix = 'contraildebug.plugins'
    module = __import__('%s.%s' % (prefix, sys.argv[1]), fromlist='_')
    module.main(args)


if __name__ == '__main__':
    sys.exit(main())
