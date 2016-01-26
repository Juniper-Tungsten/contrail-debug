import logging

from fabric.api import sudo, hide, settings

from cluster import get_all_hosts_in_cluster
from constants import SSH_PUBKEY_FILE
from exception import SetupIssue


log = logging.getLogger('contraildebug.contrail.common.cores')


def check_contrail_cores(nodes='all'):
    failure = False
    if nodes == 'all':
        nodes = get_all_hosts_in_cluster()
    for node in nodes:
        with settings(hide('everything'),
                      host_string=node,
                      key_filename=SSH_PUBKEY_FILE):
            crashes = sudo('ls /var/crashes/')
            if crashes:
                log.error('========== %s ===========\n%s' % (node, crashes))
                failure = True
    if failure:
        raise SetupIssue()
    log.info("No cores found in the cluster.")
