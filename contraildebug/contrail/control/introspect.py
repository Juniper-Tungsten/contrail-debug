import logging

import utils
from contraildebug.contrail.common.introspect import Inspect, XmlDrv

log = logging.getLogger('contraildebug.contrail.config.introspect')


class ControlInspect(Inspect):
    obj_path = {'rt': 'Snh_ShowRouteReq?x='}
    xml_path = {'rt': './tables/list/ShowRouteTable'}

    def __init__(self, ip):
        port = utils.get_control_listen_port()
        super(ControlInspect, self).__init__(ip, port, drv=XmlDrv)
        self.vrf_obj = dict()

    def get_path(self, obj_type, obj_id, **kwargs):
        return self.obj_path[obj_type]+obj_id

    def process_response(self, xml, obj_type, obj_id=None, match=None):
        obj_list = list()
        if not match:
            match = 'uuid'
        elements = xml.xpath(self.xml_path[obj_type])
        for element in elements:
            obj_list.append(self.elem2dict(element))
        if obj_id:
            for obj in obj_list:
                if obj.get(match, None) == obj_id:
                    return obj
            else:
                return None
        return obj_list

    def get_matching_routes(self, vrf_name, prefix, plen, af):
        rt_dict = {'v4': '.inet.0', 'v6': '.inet6.0',
                   'evpn': '.evpn.0'}
        routes = self.get('rt', vrf_name+rt_dict[af],
                          match='routing_table_name')['routes']['list']
        for route in routes:
            if route['prefix'] == prefix+'/'+str(plen):
                return route['paths']['list']
        else:
            return []

    def verify_prefix(self, vrf_name, prefix, label, nh_type, nh_value):
        for path in self.get_matching_routes(vrf_name, prefix,
                                             plen=32, af='v4'):
            if path['label'] == label and path[nh_type] == nh_value:
                log.info('Route for prefix %s found with label %s' % (
                         prefix, label))
                return True
        else:
            log.error("Route for prefix %s doesnt exist"
                     "or has wrong index %s or nh" % (prefix, label))
            return False

    def verify_vm(self, vm_id, vmis, agent):
        for (vmi_id, vmi_obj) in vmis.iteritems():
            vrf = ':'.join(vmi_obj['ri'][0]['to'])
            for prefix in vmi_obj['ip']:
                log.info("Verifying prefix %s with label %s"
                         "and nh %s in vrf %s" % (
                             prefix, vmi_obj['label'], agent, vrf))
                self.verify_prefix(vrf, prefix, vmi_obj['label'],
                                   'next_hop', agent)
