import json
import requests
from lxml import etree


class JsonDrv(object):
    def __init__(self, auth_token=None):
        self._headers = None
        if auth_token:
            self._headers = {'X-AUTH-TOKEN': auth_token}

    def load(self, url):
        resp = requests.get(url, headers=self._headers)
        if resp.status_code == 200:
            return json.loads(resp.text)
        return None

class XmlDrv(object):
    def load(self, url):
        return etree.fromstring(requests.get(url).text)

class Inspect(object):
    def __init__(self, ip, port, drv=JsonDrv, **kwargs):
        super(Inspect, self).__init__()
        self.ip = ip
        self.port = int(port)
        self.drv = drv(**kwargs)
        self.log = log(self).logger

    def _mk_url_str(self, path=''):
        if path.startswith('http:'):
            return path
        return "http://%s:%d/%s" % (self.ip, self.port, path)

    def http_get(self, path):
        return self.drv.load(self._mk_url_str(path))

    def get_path(self, obj_type, **kwargs):
        raise NotImplementedError

    def process_response(self, resp, **kwargs):
        return resp

    def elem2dict(self, node, alist=False):
        d = list() if alist else dict()
        for e in node.iterchildren():
            #key = e.tag.split('}')[1] if '}' in e.tag else e.tag
            if e.tag == 'list':
                value = self.elem2dict(e, alist=True)
            else:
                value = e.text if e.text else self.elem2dict(e)
            if type(d) == type(list()):
                d.append(value)
            else:
                d[e.tag] = value
        return d

    def get(self, obj_type, obj_id, match=None, **kwargs):
        if not getattr(self, obj_type+'_obj', None):
            setattr(self, obj_type+'_obj', dict())
        obj = getattr(self, obj_type+'_obj')
        if obj_id in obj:
            return obj[obj_id]
        resp = self.http_get(self.get_path(obj_type=obj_type, obj_id=obj_id, **kwargs))
        obj[obj_id] = self.process_response(resp, obj_type=obj_type, obj_id=obj_id, match=match)
        return obj[obj_id]
