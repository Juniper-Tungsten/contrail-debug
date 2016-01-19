""" Script to setup passwordless SSH from the localhost to
all other hosts in the cluster
"""
import sys


def add_sub_command(sub_parser):
    syncsshkeys_parser = sub_parser.add_parser('syncsshkeys')
    syncsshkeys_parser.add_argument('-x', type=int, default=1)


def main(self):
    pass

if __name__ == '__main__':
    sys.exit(main())
