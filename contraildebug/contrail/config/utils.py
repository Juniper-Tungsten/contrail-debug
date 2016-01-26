from vnc_cfg_api_server.utils import parse_args

from contraildebug.contrail.common.constants import API_CONF_FILE
from contraildebug.contrail.common.constants import DISCOVERY_CONF_FILE


def get_api_listen_port():
    args, _ = parse_args('--conf_file %s' % API_CONF_FILE)
    return args.listen_port


def get_discovery_listen_port():
    args, _ = parse_args('--conf_file %s' % DISCOVERY_CONF_FILE)
    return args.listen_port
