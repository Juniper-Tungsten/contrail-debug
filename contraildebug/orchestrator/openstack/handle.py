from neutronclient.neutron import client as network_client
from novaclient import client as compute_client
from keystoneclient.v2_0 import client as auth_client

from vnc_cfg_api_server.utils import parse_args

from contraildebug.common.constants import AUTH_CONF_FILE


class HandleBase(object):
    def __init__(self, args):
        self.args, _ = parse_args('--conf_file %s' % AUTH_CONF_FILE)
        # TODO: Consider taking commandline tenant name as well
        self.tenant = self.args.admin_tenant_name
        self.auth_url = '%s://%s:%d/v2.0' % (self.args.auth_protocol,
                                             self.args.auth_host,
                                             self.auth_port)


class AuthService(HandleBase):
    def get_handle(self):
        auth_handle = auth_client.Client(username=self.args.admin_user,
                                         password=self.args.admin_password,
                                         tenant_name=self.args.tenant,
                                         auth_url=self.auth_url,
                                         insecure=True)
        return auth_handle

    def get_auth_token(self):
        auth_handle = self.get_handle()
        return auth_handle.auth_token


class NetworkService(HandleBase):
    def get_handle(self):
        return network_client.Client('2.0',
                                     auth_url=self.auth_url,
                                     username=self.args.admin_user,
                                     password=self.args.admin_password,
                                     tenant_name=self.args.tenant,
                                     insecure=True)


class ComputeService(HandleBase):
    def get_handle(self):
        auth_handle = AuthService.get_handle()
        compute_handle = compute_client.Client(
                                '2',
                                auth_url=self.auth_url,
                                username=self.args.admin_user,
                                api_key=self.args.admi_password,
                                project_id=self.args.tenant,
                                auth_token=auth_handle.get_auth_token(),
                                insecure=True)
        return compute_handle
