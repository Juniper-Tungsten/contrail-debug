import utils
import logging
from contraildebug.contrail.common.introspect import Inspect, XmlDrv

log = logging.getLogger('contraildebug.contrail.compute.introspect')


class AgentInspect(Inspect):
    obj_path = {'vmi': 'Snh_PageReq?x=begin:-1,end:-1,table:db.interface.0',
                'vn': 'Snh_PageReq?x=begin:-1,end:-1,table:db.vn.0', }
    xml_path = {
            'vn': './VnListResp/vn_list/list/VnSandeshData',
            'vmi': './ItfResp/itf_list/list/ItfSandeshData',
            'v4': './Inet4UcRouteResp/route_list/list/RouteUcSandeshData', }

    def __init__(self, ip):
        port = utils.get_agent_listen_port()
        super(AgentInspect, self).__init__(ip, port, drv=XmlDrv)
        self.vrf_obj = dict()

    def get_path(self, obj_type, **kwargs):
        return self.obj_path[obj_type]

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

    def get_active_control_node(self):
        response = self.http_get('Snh_AgentXmppConnectionStatusReq?')
        for node in response.xpath('./peer/list/AgentXmppData'):
            if node.find('cfg_controller').text.lower() == 'yes':
                return node.find('controller_ip').text
        raise RuntimeError("No control-node has active XMPP connection"
                           " to compute: %s" % self.ip)

    def get_vmi(self, vmi_id, field=None):
        vmi = self.get('vmi', vmi_id)
        return vmi[field] if field else vmi

    def verify_vmi_links(self, vmi_id, ri_name, address):
        if self.get_vmi(vmi_id, 'vrf_name') != ri_name:
            log.error('VMI doesnt have link to vrf')
        else:
            log.info('VMI has vrf set')
        if self.get_vmi(vmi_id, 'ip_addr') in address:
            log.info('VMI has ip address set')
        else:
            log.error('VMI doesnt have ip address set')

    def fetch_routes(self, vrf, af='v4'):
        rt_dict = {'v4': 'uc.route.0', 'v6': 'uc.route6.0',
                   'evpn': 'evpn.route.0', 'l2': 'l2.route.0'}
        if vrf+af in self.vrf_obj:
            return self.vrf_obj[vrf+af]
        xml = self.http_get('Snh_PageReq?x=begin:-1,end:-1,table:%s.%s' %
                            (vrf, rt_dict[af]))
        self.vrf_obj[vrf+af] = xml
        return self.process_response(xml, af)

    def get_matching_routes(self, vrf_name, prefix, plen, af):
        routes = self.fetch_routes(vrf_name, af)
        for route in routes:
            if route['src_ip'] == prefix and route['src_plen'] == str(plen):
                return route['path_list']['list']
        else:
            log.error('Unable to find route with prefix %s and plen %s in vrf' %
                     (prefix, str(plen)), vrf_name)
            return []

    def verify_prefix(self, vrf_name, prefix, label, nh_type, nh_value):
        for path in self.get_matching_routes(vrf_name, prefix,
                                             plen=32, af='v4'):
            if (path['label'] == label and
                    path['nh']['NhSandeshData'][nh_type] == nh_value):
                log.info('Route for prefix %s found with label %s' %
                         (prefix, label))
                return True
        else:
            log.error('Route for prefix %s doesnt exist or has wrong index %s' %
                     (prefix, label))
            return False

    def verify_vm(self, vm_id, vmis):
        for (vmi_id, vmi_obj) in vmis.iteritems():
            ri = self.get('vn', vmi_obj['vn'][0]['uuid'])
            if ri and ri['vrf_name'] == ':'.join(vmi_obj['ri'][0]['to']):
                log.info('VN has link to RI')
            else:
                log.error('VN doesnt have link to RI')
            self.verify_vmi_links(vmi_id, ri['vrf_name'], vmi_obj['ip'])
            intf = self.get_vmi(vmi_id, 'name')
            label = self.get_vmi(vmi_id, 'label')
            for prefix in vmi_obj['ip']:
                log.info('Verifying prefix %s with label %s'
                         'and nh %s in vrf %s' %
                         (prefix, label, intf, ri['vrf_name']))
                self.verify_prefix(ri['vrf_name'], prefix, label,
                                   nh_type='itf', nh_value=intf)
