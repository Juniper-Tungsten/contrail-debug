import os
import logging
import paramiko

from fabric.api import sudo, hide
from fabric.contrib.files import append
from fabric.context_managers import settings

from contraildebug.contrail.common.constants import SSH_PUBKEY_FILE


log = logging.getLogger("contraildebug.utils.sshutil")


def ssh(host, user, password=None, key_filename=SSH_PUBKEY_FILE):
    """ SSH to any host.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if password:
        ssh.connect(host, username=user, password=password)
    elif key_filename:
        ssh.connect(host, username=user, key_filename=key_filename)
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
    if os.path.isfile(SSH_PUBKEY_FILE):
        log.debug("SSH Public key is present in localhost")
        return True
    else:
        log.debug("SSH Public key is not present in localhost")
        return False


def ssh_keygen():
    """ Generates SSH keys.
    """
    log.debug("Generating SSH keys")
    os.system('yes | ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""')
    log.debug("Generated SSH keys")


def copy_public_key(target_ip, username, password):
    """ Copies over public key of localhost to the authorized_keys
    file of the specified host.
    """
    with open(SSH_PUBKEY_FILE, 'r') as fd:
        public_key = fd.read()
    with settings(hide('everything'),
                  host_string='%s@%s' % (username, target_ip),
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
    log.debug("Keys already generated.")
    log.info("Sync in progress ...")
    for host in hosts:
        log.debug("Copying SSH public key to host: %s" % host)
        copy_public_key(host, username, password)
    log.info("Sync Complete")
