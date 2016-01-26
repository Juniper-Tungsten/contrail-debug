import logging

from contraildebug.contrail.common.cluster import get_config_hosts
from contraildebug.orchestrator.vn import OrchVnDiag
from contraildebug.orchestrator.vm import OrchVmDiag
from contraildebug.contrail.config.introspect import ApiServerInspect
from contraildebug.contrail.control.introspect import ControlInspect
from contraildebug.contrail.compute.introspect import AgentInspect

log = logging.getLogger('contraildebug.contrail.contrail.vm')


def verify_vm(vm_id, tenant='admin'):
    vn_diag = OrchVnDiag(tenant)
    vm_diag = OrchVmDiag()

    vn_ids = vn_diag.get_vn_ids(vm_id)
    vm_ips = vm_diag.get_vm_ips(vm_id)
    vn_fq_names = [vn_diag.get_vn_obj(vn_id)['contrail:fq_name']
                   for vn_id in vn_ids]
    ri_names = [':'.join(vn+vn[-1:]) for vn in vn_fq_names]

    # Verify in config node
    for config in get_config_hosts():
        api_server = ApiServerInspect(config)
        api_server.verify_vn_links(vm_id, [':'.join(vn) for vn in vn_fq_names])
        api_server.verify_ip_assigned(vm_id, vm_ips)
        api_server.verify_ri_links(vm_id, ri_names)
    port_objs = api_server.get_port_mappings(vm_id)

    # Verify in agent
    agent_host = vm_diag.get_host_of_vm(vm_id)
    agent = AgentInspect(agent_host)
    agent.verify_vm(vm_id, port_objs)
    for vmi_id, port_obj in port_objs.iteritems():
        port_obj['label'] = agent.get_vmi(vmi_id, 'label')

    # Verify in control
    control_host = agent.get_active_control_node()
    control = ControlInspect(control_host)
    control.verify_vm(vm_id, port_objs, agent_host)
