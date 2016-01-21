from fabric.api import local, sudo
import os
import logging

from fabric.files import append
from fabric.context_managers import settings

from contraildebug.common.constants import SSH_PUBKEY_FILE


log = logging.getLogger("contraildebug.utils.sshutil")


def ssh(host, user, password=None, key_filename=SSH_PUBKEY_FILE):
    """ SSH to any host.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password:
        ssh.connect(host, username=user, password=password)
    elif key_filename:
        ssh.connect(host, username=user, key_filename=key_filenme)
    return ssh


def execute(cmd, ssh):
    """Executing command over SSH
    """
    out = None
    err = None
    log.debug("Executing command: %s" % cmd)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read()
    err = stderr.read()
    return (out, err)


def public_key_present():
    """ Checks whether the SSH public key is already created.
    """
    if os.path.isfile('~/.ssh/id_rsa.pub'):
        log.debug("SSH Public key is present")
        return True
    else:
        log.debug("SSH Public key is not present")
        return False


def ssh_keygen():
    """ Generates SSH keys.
    """
    local('ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""')
    log.debug("Generated SSH keys")


def copy_public_key(target_ip, username, password):
    """ Copies over public key of localhost to the authorized_keys
    file of the specified host.
    """
    public_key = local('cat ~/.ssh/id_rsa.pub', capture=True)
    with settings(host_string='%s@%s' % (username, target_ip),
                  password=password):
        append('~/.ssh/authorized_keys', public_key, use_sudo=True)
        sudo('chmod 640 ~/.ssh/authorized_keys')
    log.debug("Copied SSH public key to host: %s" % target_ip)


def setup_passwordless_login(hosts, username, password):
    """ Copies over public key of localhost to the list of hosts specified.
    Thus enables passwordless SSH from localhost to the list of hosts
    """
    if not public_key_present():
        ssh_keygen()
    for host in hosts:
        log.debug("Copying SSH public key to host: %s" % host)
        copy_public_key(host, username, password)
