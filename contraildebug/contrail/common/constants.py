import os


# SSH
SSH_PUBKEY_FILE = os.path.expanduser('~/.ssh/id_rsa.pub')

# Config files
AUTH_CONF_FILE = '/etc/contrail/contrail-keystone-auth.conf'
API_CONF_FILE = '/etc/contrail/contrail-api.conf'
DISCOVERY_CONF_FILE = '/etc/contrail/contrail-discovery.conf'

# Service ports
CONTROL_LISTEN_PORT = 8083
AGENT_LISTEN_PORT = 8085
