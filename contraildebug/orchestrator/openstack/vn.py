import logging

from contraildebug.orchestrator.openstack.main import OpenstackDiag

log = logging.getLogger('contraildebug.orchestraor.openstack.vm')


class OpenstackVnDiag(OpenstackDiag):
    def __init__(self, tenant='admin'):
        super(OpenstackVnDiag, self).__init__(tenant)
        self.vn_obj = dict()

    def get_vn_ids(self, vn_names):
        vn_objs = self.network_handle.list_networks(name=vn_names)['networks']
        for vn_obj in vn_objs:
            self.vn_obj[vn_obj['id']] = vn_obj
        return [vn_obj['id'] for vn_obj in self.vn_obj.itervalues()
                if vn_obj['name'] in vn_names]

    def get_vn_obj(self, vn_id):
        if vn_id not in self.vn_obj:
            self.vn_obj[vn_id] =\
                self.network_handle.show_network(vn_id)['network']
        return self.vn_obj[vn_id]
