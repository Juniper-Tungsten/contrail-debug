import logging
from collections import defaultdict

import utils
from contraildebug.contrail.common.introspect import Inspect

log = logging.getLogger('contraildebug.contrail.config.introspect')


class Discovery(Inspect):
    def __init__(self, disc_ip):
        port = utils.get_discovery_listen_port()
        super(Discovery, self).__init__(disc_ip, port)

    def get_services(self):
        services = {'xmpp-server': 'control-node',
                    'OpServer': 'analytics',
                    'ApiServer': 'config'}
        service_dict = defaultdict(list)
        for service in self.http_get('services.json')['services']:
            svc_type = services.get(service['service_type'], None)
            if not svc_type:
                continue
            service_dict[svc_type].append(service['info'])
        return service_dict


class ApiServerInspect(Inspect):
    obj_path = {'vm': 'virtual-machine',
                'vmi': 'virtual-machine-interface',
                'iip': 'instance-ip',
                'vn': 'virtual-network',
                'ri': 'routing-instance', }

    def __init__(self, ip, auth_token=None):
        port = utils.get_api_listen_port()
        super(ApiServerInspect, self).__init__(ip, port, auth_token=auth_token)
        self.port_obj = defaultdict(dict)

    def get_path(self, obj_type, obj_id, **kwargs):
        return self.obj_path[obj_type]+'/'+obj_id

    def process_response(self, resp, obj_type, **kwargs):
        return resp[self.obj_path[obj_type]]

    def get_vmis(self, vm_id):
        vmis = [vmi['uuid'] for vmi in
                self.get('vm', vm_id)['virtual_machine_interface_back_refs']]
        return [self.get('vmi', vmi) for vmi in vmis]

    def get_ip_address(self, vmi_id):
        if vmi_id not in self.vmi_obj:
            self.get('vmi', vmi_id)
        iips = [iip['uuid']
                for iip in self.vmi_obj[vmi_id]['instance_ip_back_refs']]
        return [self.get('iip', iip)['instance_ip_address'] for iip in iips]

    def verify_ip_assigned(self, vm_id, expected_ips=[]):
        assigned_ips = list()
        vmis = self.get_vmis(vm_id)
        for vmi in vmis:
            assigned_ips.extend(self.get_ip_address(vmi['uuid']))
        if (assigned_ips and
                (not expected_ips or
                    set(expected_ips) == set(assigned_ips))):
            log.info('VM have IP address assigned')
        else:
            log.error('VM doesnt have expected IP address, expected %s'
                     ', assigned %s' % (expected_ips, assigned_ips))

    def verify_ri_links(self, vm_id, expected_ris=[]):
        assigned_ris = list()
        vmis = self.get_vmis(vm_id)
        for vmi in vmis:
            ris = [ri['uuid'] for ri in vmi['routing_instance_refs']]
            assigned_ris.extend([':'.join(self.get('ri', ri)['fq_name'])
                                for ri in ris])
        if (assigned_ris and
                (not expected_ris or
                    set(expected_ris) == set(assigned_ris))):
            log.info('VMI have RI link')
        else:
            log.error('VMI doesnt have RI refs')

    def verify_vn_links(self, vm_id, expected_vns=[]):
        assigned_vns = list()
        vmis = self.get_vmis(vm_id)
        for vmi in vmis:
            vns = [vn['uuid'] for vn in vmi['virtual_network_refs']]
            assigned_vns.extend([':'.join(self.get('vn', vn)['fq_name'])
                                for vn in vns])
        if (assigned_vns and
                (not expected_vns or
                    set(expected_vns) == set(assigned_vns))):
            log.info('VMI have link to VN')
        else:
            log.error('VMI doesnt have VN refs')

    def get_port_obj(self, vmi_id):
        self.port_obj[vmi_id['uuid']]['vn'] = vmi_id['virtual_network_refs']
        self.port_obj[vmi_id['uuid']]['ri'] = vmi_id['routing_instance_refs']
        self.port_obj[vmi_id['uuid']]['ip'] =\
            self.get_ip_address(vmi_id['uuid'])
        return self.port_obj[vmi_id['uuid']]

    def get_port_mappings(self, vm_id):
        vmis = self.get_vmis(vm_id)
        port_objs = dict()
        for vmi in vmis:
            port_objs[vmi['uuid']] = self.get_port_obj(vmi)
        return port_objs
