import logging
import importlib


from contraildebug.contrail.common.cluster import get_orch


log = logging.getLogger('contraildebug.orchestrator.vn')


orch = get_orch()
orch_cap = orch[:1].upper() + orch[1:]
try:
    vn = importlib.import_module('contraildebug.orchestrator.%s.vn' % orch)
    VnDiag = getattr(vn, '%sVnDiag' % orch_cap)
except:
    log.error("Orchestrator %s is not Implemented" % orch)
    raise


class OrchVnDiag(VnDiag):
    pass
