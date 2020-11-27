# Install
```shell script
pip install -U namekox-consul
```

# Example
```python
# ! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


from namekox_consul.core.allotter import Allotter
from namekox_webserver.core.entrypoints.app import app
from namekox_consul.core.dependencies import ConsulHelper
from namekox_consul.constants import DEFAULT_CONSUL_SERVICE_ROOT_PATH


class Ping(object):
    name = 'ping'

    # https://python-consul.readthedocs.io/en/latest/
    # ConsulHelper(
    #       dbname,
    #       serverid=None,
    #       watching=None,
    #       allotter=None,
    # https://python-consul.readthedocs.io/en/latest/#consul.Consul
    #       coptions=None,
    # https://python-consul.readthedocs.io/en/latest/#consul.base.Consul.Agent.Service.register
    #       roptions=None)
    consul = ConsulHelper(name, allotter=Allotter(), watching=DEFAULT_CONSUL_SERVICE_ROOT_PATH)

    @app.api('/api/assign/server/', methods=['GET'])
    def assign_server(self, request):
        return self.consul.allotter.get(self.name)
```

# Running
> config.yaml
```yaml
CONSUL:
  ping:
    host: 127.0.0.1
    port: 8500
WEBSERVER:
  host: 0.0.0.0
  port: 80
```
> namekox run ping
```shell script
2020-11-27 18:51:30,678 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-27 18:51:30,679 DEBUG starting services ['ping']
2020-11-27 18:51:30,680 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-11-27 18:51:30,683 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-11-27 18:51:30,683 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2020-11-27 18:51:30,684 DEBUG starting service ping dependencies [ping:namekox_consul.core.dependencies.ConsulHelper:consul]
2020-11-27 18:51:30,706 DEBUG Starting new HTTP connection (1): 127.0.0.1:8500
2020-11-27 18:51:30,713 DEBUG http://127.0.0.1:8500 "PUT /v1/agent/service/register HTTP/1.1" 200 0
2020-11-27 18:51:30,715 DEBUG service ping dependencies [ping:namekox_consul.core.dependencies.ConsulHelper:consul] started
2020-11-27 18:51:30,715 DEBUG services ['ping'] started
2020-11-27 18:51:32,709 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10e0f48d0>, ('127.0.0.1', 64394)), kwargs={}, tid=handle_request)
2020-11-27 18:51:34,414 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10e0f4610>, ('127.0.0.1', 64398)), kwargs={}, tid=handle_request)
2020-11-27 18:51:34,417 DEBUG spawn worker thread handle ping:assign_server(args=(<Request 'http://127.0.0.1/api/assign/server/' [GET]>,), kwargs={}, context={})
2020-11-27 18:51:34,420 DEBUG http://127.0.0.1:8500 "GET /v1/health/service/namekox/ping?passing=1 HTTP/1.1" 200 628
127.0.0.1 - - [27/Nov/2020 18:51:34] "GET /api/assign/server/ HTTP/1.1" 200 269 0.006768
2020-11-27 18:51:37,710 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x10e0f46d0>, ('127.0.0.1', 64408)), kwargs={}, tid=handle_request)
^C2020-11-27 18:51:39,661 DEBUG stopping services ['ping']
2020-11-27 18:51:39,661 DEBUG stopping service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-11-27 18:51:39,662 DEBUG wait service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stop
2020-11-27 18:51:39,663 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] stopped
2020-11-27 18:51:39,663 DEBUG stopping service ping dependencies [ping:namekox_consul.core.dependencies.ConsulHelper:consul]
2020-11-27 18:51:39,669 DEBUG http://127.0.0.1:8500 "PUT /v1/agent/service/deregister/8cd53729-dd62-4dd9-b402-d9e0377058c4 HTTP/1.1" 200 0
2020-11-27 18:51:39,670 DEBUG service ping dependencies [ping:namekox_consul.core.dependencies.ConsulHelper:consul] stopped
2020-11-27 18:51:39,670 DEBUG services ['ping'] stopped
2020-11-27 18:51:39,670 DEBUG killing services ['ping']
2020-11-27 18:51:39,670 DEBUG service ping already stopped
2020-11-27 18:51:39,671 DEBUG services ['ping'] killed
```
> curl http://127.0.0.1/api/assign/server/
```json
{
    "errs": "", 
    "code": "Request:Success", 
    "data": {
        "port": 80,
        "address": "127.0.0.1"
    }, 
    "call_id": "cc910b95-dd07-496f-8a9f-c9304cfb5cd3"
}
```

# Debug
> config.yaml
```yaml
CONTEXT:
  - namekox_consul.cli.subctx.consul:Consul
CONSUL:
  ping:
    host: 127.0.0.1
    port: 8500
WEBSERVER:
  host: 0.0.0.0
  port: 80
```
> namekox shell
```shell script
In [1]: nx.consul.proxy('ping').health.service('namekox/ping', passing=True)
2020-11-27 18:53:03,591 DEBUG Starting new HTTP connection (1): 127.0.0.1:8500
2020-11-27 18:53:03,593 DEBUG http://127.0.0.1:8500 "GET /v1/health/service/namekox/ping?passing=1 HTTP/1.1" 200 628
Out[1]:
('1026',
 [{u'Checks': [{u'CheckID': u'serfHealth',
     u'CreateIndex': 12,
     u'Definition': {},
     u'ModifyIndex': 12,
     u'Name': u'Serf Health Status',
     u'Node': u'manmanli.local',
     u'Notes': u'',
     u'Output': u'Agent alive and reachable',
     u'ServiceID': u'',
     u'ServiceName': u'',
     u'ServiceTags': [],
     u'Status': u'passing',
     u'Type': u''},
    {u'CheckID': u'service:507ee897-2e44-4911-98c9-21506f525bbf',
     u'CreateIndex': 1025,
     u'Definition': {},
     u'ModifyIndex': 1026,
     u'Name': u"Service 'namekox/ping' check",
     u'Node': u'manmanli.local',
     u'Notes': u'',
     u'Output': u'TCP connect 127.0.0.1:80: Success',
     u'ServiceID': u'507ee897-2e44-4911-98c9-21506f525bbf',
     u'ServiceName': u'namekox/ping',
     u'ServiceTags': [],
     u'Status': u'passing',
     u'Type': u'tcp'}],
   u'Node': {u'Address': u'127.0.0.1',
    u'CreateIndex': 12,
    u'Datacenter': u'dc1',
    u'ID': u'4bda6e77-f59c-045e-5e57-40c314f708a3',
    u'Meta': {u'consul-network-segment': u''},
    u'ModifyIndex': 13,
    u'Node': u'manmanli.local',
    u'TaggedAddresses': {u'lan': u'127.0.0.1',
     u'lan_ipv4': u'127.0.0.1',
     u'wan': u'127.0.0.1',
     u'wan_ipv4': u'127.0.0.1'}},
   u'Service': {u'Address': u'127.0.0.1',
    u'Connect': {},
    u'CreateIndex': 1025,
    u'EnableTagOverride': False,
    u'ID': u'507ee897-2e44-4911-98c9-21506f525bbf',
    u'Meta': None,
    u'ModifyIndex': 1025,
    u'Port': 80,
    u'Proxy': {u'Expose': {}, u'MeshGateway': {}},
    u'Service': u'namekox/ping',
    u'TaggedAddresses': {u'lan_ipv4': {u'Address': u'127.0.0.1', u'Port': 80},
     u'wan_ipv4': {u'Address': u'127.0.0.1', u'Port': 80}},
    u'Tags': [],
    u'Weights': {u'Passing': 1, u'Warning': 1}}}])
```
