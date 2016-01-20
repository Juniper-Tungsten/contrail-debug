import logging

from vnc_cfg_api_server.utils import parse_args
from vnc_api.vnc_api import VncApi

import utils
from contraildebug.common.constants import AUTH_CONF_FILE


log = logging.getLogger('contraildebug.config.handle')


class VncApiService(object):
    def __init__(self, tenant=None):
        self.args, _ = parse_args('--conf_file %s' % AUTH_CONF_FILE)
        if not tenant:
            self.tenant_name = self.args.admin_tenant_name
        else:
            self.tenant_name = tenant

    def get_handle(self):
        api_handle = VncApi(username=self.args.admin_user,
                            password=self.args.admin_password,
                            tenant_name=self.tenant_name,
                            api_server_host='127.0.0.1',
                            api_server_port=utils.get_api_listen_port())

        return api_handle
