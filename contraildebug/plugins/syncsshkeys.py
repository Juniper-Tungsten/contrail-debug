""" Script to setup passwordless SSH from the localhost to
all other hosts in the cluster
"""
import sys
import logging
import getpass
import argparse

from contraildebug.utils.sshutil import setup_passwordless_login
from contraildebug.contrail.common.cluster import get_all_hosts_in_cluster


log = logging.getLogger('contraildebug.scripts.syncsshkeys')


def add_sub_command(parser):
    if isinstance(parser, argparse._SubParsersAction):
        syncsshkeys_parser = parser.add_parser('syncsshkeys')
    elif isinstance(parser, argparse.ArgumentParser):
        syncsshkeys_parser = parser
    syncsshkeys_parser.add_argument(
            '-n', '--nodes', dest='nodes', nargs='+', type=str,
            default=get_all_hosts_in_cluster(),
            help="Copies over the public key to these nodes.")
    syncsshkeys_parser.add_argument(
            '-u', '--user', dest='user', default='root', type=str,
            help="User of the nodes.")
    syncsshkeys_parser.add_argument(
            '-p', '--password', dest='password', default=None, type=str,
            help="Password of the nodes.")

    return syncsshkeys_parser


def parse_args(args_str):
    parser = argparse.ArgumentParser()
    parser = add_sub_command(parser)
    args = parser.arg_parse()
    return args


def main(args):
    password = args.password
    if not password:
        password = getpass.getpass()
    # Sync SSH public keys
    setup_passwordless_login(args.nodes, args.user, password)

if __name__ == '__main__':
    sys.exit(main(parse_args(sys.argv[1:])))
