import os
import logging
from collections import OrderedDict

from contraildebug.contrail.config.handle import VncApiService
from contraildebug.contrail.common.constants import AUTH_CONF_FILE


log = logging.getLogger('contraildebug.contrail.common.cluster')


def get_orch():
    orch = 'unsupported'
    if os.path.exists(AUTH_CONF_FILE):
        orch = 'openstack'

    return orch


def get_hosts(method_prefix):
    api_client = VncApiService().get_handle()
    hosts_list_method = getattr(api_client, '%ss_list' % method_prefix)
    host_read_method = getattr(api_client, '%s_read' % method_prefix)
    host_dict_list = hosts_list_method()[method_prefix.replace('_', '-') + 's']
    hosts = list()
    for host_dict in host_dict_list:
        host_obj = host_read_method(host_dict['fq_name'])
        if method_prefix == 'bgp_router':
            vendor = getattr(host_obj.bgp_router_parameters, 'vendor')
            if vendor == 'contrail':
                host_ip_address = getattr(host_obj.bgp_router_parameters,
                                          'address')
        else:
            host_ip_address = getattr(host_obj,
                                      '%s_ip_address' % method_prefix)
        hosts.append(str(host_ip_address))

    return hosts


def get_config_hosts():
    return get_hosts('config_node')


def get_database_hosts():
    return get_hosts('database_node')


def get_collector_hosts():
    return get_hosts('analytics_node')


def get_control_hosts():
    return get_hosts('bgp_router')


def get_webui_hosts():
    pass


def get_compute_hosts():
    return get_hosts('virtual_router')


def get_topology():
    topology = OrderedDict()
    topology['config'] = get_config_hosts()
    topology['database'] = get_database_hosts()
    topology['collector'] = get_collector_hosts()
    topology['control'] = get_control_hosts()
    # topology['webui'] = get_webui_hosts()
    topology['compute'] = get_compute_hosts()

    return topology


def get_all_hosts_in_cluster():
    all_hosts = list()
    for role, hosts in get_topology().items():
        all_hosts.extend(hosts)

    return list(set(all_hosts))
