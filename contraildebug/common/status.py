import logging

from fabric.api import local, sudo, hide, settings

from cluster import get_all_hosts_in_cluster


log = logging.getLogger('contraildebug.common.status')


def check_contrail_status(nodes='all'):
    if nodes == 'all':
        nodes = get_all_hosts_in_cluster()
    for node in nodes:
        with settings(hide('everything'), host_string=node):
            status = sudo('contrail-status')
            log.info('========== %s ===========\n%s' % (node, status))
