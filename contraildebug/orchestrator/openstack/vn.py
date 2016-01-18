from contraildebug.orchestrator.openstack.main import Openstack


class VirtualNetwork(Openstack):
    def __init__(self):
        super(VirtualNetwork, self).__init__()
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
