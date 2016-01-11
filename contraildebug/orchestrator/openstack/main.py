class Openstack(object):
    def __init__(self):
        self.auth_handle = AuthService.get_handle()
        self.network_handle = NetworkService.get_handle()
        self.compute_handle = ComputeService.get_handle()

    def get_hosts(self):
        self.hosts = dict()
        pattern = "http://(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:(?P<port>\d+))?"
        services = ('network', 'compute')
        for service in services:
            uris = self.auth_handle.service_catalog.get_endpoints(service)\
                       [service]
            self.hosts[service] = [
                re.match(pattern,
                uri['publicURL']).group('ip') for uri in uris]
        self.hosts['agent'] = self.get_hypervisor_list()

    def get_hypervisor_list(self):
        hosts = list()
        for host_info in self.network_handle.hypervisors.list(detailed=True):
            hosts.append(host_info.host_ip)
            self.host_name_map[host_info.hypervisor_hostname] = host_info.host_ip
        return hosts

    def get_network_hosts(self):
        return self.hosts['network']

    def get_compute_hosts(self):
        return self.hosts['compute']

    def get_hypervisors(self):
        return self.hosts['agent']
