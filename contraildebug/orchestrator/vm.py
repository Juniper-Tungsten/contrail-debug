import logging
import importlib


from contraildebug.contrail.common.cluster import get_orch


log = logging.getLogger('contraildebug.orchestrator.vm')


orch = get_orch()
orch_cap = orch[:1].upper() + orch[1:]
try:
    vm = importlib.import_module('contraildebug.orchestrator.%s.vm' % orch)
    VmDiag = getattr(vm, '%sVmDiag' % orch_cap)
except:
    log.error("Orchestrator %s is not Implemented" % orch)
    raise


class OrchVmDiag(VmDiag):
    pass
