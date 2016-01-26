import logging

from fabric.api import sudo, hide, settings

from cluster import get_all_hosts_in_cluster
from constants import SSH_PUBKEY_FILE
from exception import SetupIssue


log = logging.getLogger('contraildebug.contrail.common.status')
FAIL_STATUS = ('failed', 'initializing', 'dead', 'down')


def check_contrail_status(nodes='all'):
    failure = False
    if nodes == 'all':
        nodes = get_all_hosts_in_cluster()
    for node in nodes:
        with settings(hide('everything'),
                      host_string=node,
                      key_filename=SSH_PUBKEY_FILE):
            status = sudo('contrail-status')
            msg = '========== %s ===========\n%s' % (node, status)
            if any(fail_status in status for fail_status in FAIL_STATUS):
                log.error(msg)
                failure = True
            else:
                log.debug(msg)
    if failure:
        raise SetupIssue()
    log.info("All contrail services are running.")
