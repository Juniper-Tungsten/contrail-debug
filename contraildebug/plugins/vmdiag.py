""" Script to diagnose the Virtual Machine.
"""
import sys
import argparse
import logging

from contraildebug.orchestrator.vm import OrchVmDiag
from contraildebug.contrail.vm import verify_vm


log = logging.getLogger('contraildebug.scripts.vmdiag')


def add_sub_command(parser):
    if isinstance(parser, argparse._SubParsersAction):
        vmdiag_parser = parser.add_parser('vmdiag')
    elif isinstance(parser, argparse.ArgumentParser):
        vmdiag_parser = parser
    vmdiag_parser.add_argument(
            '-t', '--tenant', dest='tenant', default='admin', type=str,
            help="Project in which the VM resides.")
    vmdiag_parser.add_argument(
            '-i', '--vmid', dest='vmid', type=str,
            help="UUID of the Virtual machine.")
    vmdiag_parser.add_argument(
            '-u', '--vmuser', dest='vmuser', type=str,
            help="User in the Virtual machine.")
    vmdiag_parser.add_argument(
            '-p', '--vmpassword', dest='vmpasswd', type=str,
            help="Password of the user in the Virtual machine.")
    vmdiag_parser.add_argument(
            '-d', '--destination', dest='destination', type=str,
            help="Destination ip from the Virtual machine to be verified.")

    return vmdiag_parser


def parse_args(args_str):
    parser = argparse.ArgumentParser()
    parser = add_sub_command(parser)
    args = parser.arg_parse()
    return args


def main(args):
    vm_diag = OrchVmDiag(args.tenant)
    vm_diag.verify_vm(args.vmid)
    verify_vm(args.vmid, tenant=args.tenant)

if __name__ == '__main__':
    sys.exit(main(parse_args(sys.argv[1:])))
