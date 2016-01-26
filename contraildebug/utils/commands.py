import logging

from fabric.api import sudo, settings, hide

from contraildebug.contrail.common.constants import SSH_PUBKEY_FILE

log = logging.getLogger('contraildebug.utils.commmands')


def run_cmd_on_vm(self, cmd, compute_ip, vm_ip, vm_user, vm_password):
    fab_string = 'fab -H %s@%s -p %s -- ' % (vm_user, vm_ip, vm_password)
    host_cmd = fab_string+'"'+cmd+'"'
    with settings(hide('everything'),
                  host_string=compute_ip,
                  key_filename=SSH_PUBKEY_FILE,
                  warn_only=True):
        return sudo(host_cmd)
