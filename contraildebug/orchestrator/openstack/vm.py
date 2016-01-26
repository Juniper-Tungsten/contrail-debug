import logging

from contraildebug.orchestrator.openstack.main import OpenstackDiag

log = logging.getLogger('contraildebug.orchestraor.openstack.vm')


class OpenstackVmDiag(OpenstackDiag):
    def __init__(self, tenant='admin'):
        super(OpenstackVmDiag, self).__init__(tenant)
        self.vm_obj = dict()

    def get_vm_obj(self, vm_id):
        if vm_id not in self.vm_obj:
            self.vm_obj[vm_id] = self.compute_handle.servers.get(vm_id)
        return self.vm_obj[vm_id]

    def get_vm_name(self, vm_id):
        vm_obj = self.get_vm_obj(vm_id)
        return vm_obj.name

    def get_host_of_vm(self, vm_id):
        vm_obj = self.get_vm_obj(vm_id)
        return self.host_name_map[
                   vm_obj._info['OS-EXT-SRV-ATTR:hypervisor_hostname']]

    def get_vm_ips(self, vm_id):
        vm_obj = self.get_vm_obj(vm_id)
        assigned_ips = list()
        for vn, ips in vm_obj._info['addresses'].iteritems():
            for ip in ips:
                assigned_ips.append(ip['addr'])
        return assigned_ips

    def get_vn_names(self, vm_id):
        return self.get_vm_obj(vm_id).addresses.keys()

    def verify_vm_is_up(self, vm_id):
        vm_obj = self.get_vm_obj(vm_id)
        if vm_obj._info['status'].lower() == 'active' and \
           vm_obj._info['OS-EXT-STS:power_state'] == 1:
            log.info("VM got launched")
        else:
            log.error("VM is not launched")

    def verify_ip_assigned(self, vm_id):
        vm_ips = self.get_vm_ips(vm_id)
        if vm_ips:
            log.info('VM %s has been assigned %s' % (vm_id, str(vm_ips)))
        else:
            log.error('VM hasnt been assigned an ip address')

    def verify_vm(self, vm_id):
        self.verify_vm_is_up(vm_id)
        self.verify_ip_assigned(vm_id)
        return True
