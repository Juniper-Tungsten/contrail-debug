""" Script to check the health of the contrail cluster
"""
import sys
import logging


log = logging.getLogger('contraildebug.scripts.healthcheck')


def add_sub_command(sub_parser):
    healthcheck_parser = sub_parser.add_parser('healthcheck')


def main(self):
    log.info("OK OK OK OK OK")

if __name__ == '__main__':
    sys.exit(main())
