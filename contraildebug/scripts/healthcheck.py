""" Script to check the health of the contrail cluster
"""
import sys
import argparse
import logging

from contraildebug.common.status import check_contrail_status
from contraildebug.common.cores import check_contrail_cores


log = logging.getLogger('contraildebug.scripts.healthcheck')


def add_sub_command(parser):
    if isinstance(parser, argparse._SubParsersAction):
        healthcheck_parser = parser.add_parser('healthcheck')
    elif isinstance(parser, argparse.ArgumentParser):
        healthcheck_parser = parser
    healthcheck_parser.add_argument(
            '-n', '--nodes', dest='nodes', default='all', nargs='+', type=str,
            help="Does health check of all contrail services in the node.")

    return healthcheck_parser


def parse_args(args_str):
    parser = argparse.ArgumentParser()
    parser = add_sub_command(parser)
    args = parser.arg_parse()
    return args


def main(args):
    # Check contrail-status
    check_contrail_status(nodes=args.nodes)
    # Check for cores
    check_contrail_cores(nodes=args.nodes)

if __name__ == '__main__':
    sys.exit(main(parse_args(sys.argv[1:])))
