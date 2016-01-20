import logging

from contraildebug.config.handle import VncApiService


log = logging.getLogger('contraildebug.common.cluster')


def get_hosts(method_prefix):
    api_client = VncApiService().get_handle()
    hosts_list_method = getattr(api_client, '%ss_list' % method_prefix)
    host_read_method = getattr(api_client, '%s_read' % method_prefix)
    host_dict_list = hosts_list_method()[method_prefix.replace('_', '-') + 's']
    hosts = list()
    for host_dict in host_dict_list:
        host_obj = host_read_method(host_dict['fq_name'])
        host_ip_address = getattr(host_obj, '%s_ip_address' % method_prefix)
        hosts.append(host_ip_address)

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


def get_all_hosts_in_cluster():
    all_hosts = list()
    all_hosts.extend(get_config_hosts())
    all_hosts.extend(get_database_hosts())
    all_hosts.extend(get_collector_hosts())
    all_hosts.extend(get_control_hosts())
    # all_hosts.extend(get_webui_hosts())
    all_hosts.extend(get_compute_hosts())

    return all_hosts
