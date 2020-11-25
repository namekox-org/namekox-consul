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


class Ping(object):
    name = 'ping'

    # https://python-consul.readthedocs.io/en/latest/
    # ConsulHelper(
    #       dbname,
    #       serverid=None,
    #       allotter=None,
    # https://python-consul.readthedocs.io/en/latest/#consul.Consul
    #       coptions=None,
    # https://python-consul.readthedocs.io/en/latest/#consul.base.Consul.Agent.Service.register
    #       roptions=None)
    consul = ConsulHelper(name, allotter=Allotter())

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
2020-11-25 18:58:42,306 DEBUG load container class from namekox_core.core.service.container:ServiceContainer
2020-11-25 18:58:42,307 DEBUG starting services ['ping']
2020-11-25 18:58:42,307 DEBUG starting service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server]
2020-11-25 18:58:42,309 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_connect(args=(), kwargs={}, tid=handle_connect)
2020-11-25 18:58:42,309 DEBUG service ping entrypoints [ping:namekox_webserver.core.entrypoints.app.handler.ApiServerHandler:assign_server, ping:namekox_webserver.core.entrypoints.app.server.WebServer:server] started
2020-11-25 18:58:42,310 DEBUG starting service ping dependencies [ping:namekox_consul.core.dependencies.ConsulHelper:consul]
2020-11-25 18:58:42,329 DEBUG Starting new HTTP connection (1): 127.0.0.1:8500
2020-11-25 18:58:42,332 DEBUG http://127.0.0.1:8500 "PUT /v1/agent/service/register HTTP/1.1" 200 0
2020-11-25 18:58:42,345 DEBUG http://127.0.0.1:8500 "PUT /v1/agent/service/register HTTP/1.1" 200 0
2020-11-25 18:58:42,346 DEBUG service ping dependencies [ping:namekox_consul.core.dependencies.ConsulHelper:consul] started
2020-11-25 18:58:42,347 DEBUG services ['ping'] started
2020-11-25 18:58:46,462 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x1106ffdd0>, ('127.0.0.1', 49505)), kwargs={}, tid=handle_request)
2020-11-25 18:58:51,464 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x1106ffc50>, ('127.0.0.1', 49521)), kwargs={}, tid=handle_request)
2020-11-25 18:58:56,469 DEBUG spawn manage thread handle ping:namekox_webserver.core.entrypoints.app.server:handle_request(args=(<eventlet.greenio.base.GreenSocket object at 0x1106ffcd0>, ('127.0.0.1', 49537)), kwargs={}, tid=handle_request)
```
> curl http://127.0.0.1/api/assign/server/
```json
{
    "errs": "", 
    "code": "Request:Success", 
    "data": {
        "Node": "manmanli.local", 
        "Datacenter": "dc1", 
        "ServiceWeights": {
            "Passing": 1, 
            "Warning": 1
        }, 
        "ServiceProxy": {
            "MeshGateway": { }, 
            "Expose": { }
        }, 
        "ServiceMeta": { }, 
        "ServiceName": "namekox/ping", 
        "TaggedAddresses": {
            "wan_ipv4": "127.0.0.1", 
            "wan": "127.0.0.1", 
            "lan": "127.0.0.1", 
            "lan_ipv4": "127.0.0.1"
        }, 
        "ServiceConnect": { }, 
        "ServiceEnableTagOverride": false, 
        "ModifyIndex": 1732, 
        "CreateIndex": 1732, 
        "ServicePort": 80, 
        "ServiceID": "a96f6ba5-7b33-4b51-abb8-f184aee6fdce", 
        "ServiceAddress": "127.0.0.1", 
        "Address": "127.0.0.1", 
        "ServiceKind": "", 
        "ServiceTags": [ ], 
        "NodeMeta": {
            "consul-network-segment": ""
        }, 
        "ServiceTaggedAddresses": {
            "wan_ipv4": {
                "Port": 80, 
                "Address": "127.0.0.1"
            }, 
            "lan_ipv4": {
                "Port": 80, 
                "Address": "127.0.0.1"
            }
        }, 
        "ID": "745b4472-a2f8-c430-0521-5eaffdcf3e17"
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
In [1]: nx.consul.proxy('ping').catalog.service('namekox/ping')
2020-11-25 19:20:06,656 DEBUG Starting new HTTP connection (1): 127.0.0.1:8500
2020-11-25 19:20:06,659 DEBUG http://127.0.0.1:8500 "GET /v1/catalog/service/namekox/ping HTTP/1.1" 200 1249
Out[1]:
('31',
 [{u'Address': u'127.0.0.1',
   u'CreateIndex': 29,
   u'Datacenter': u'dc1',
   u'ID': u'74caaf27-cc1f-99cd-dda2-b482279766cf',
   u'ModifyIndex': 29,
   u'Node': u'manmanli.local',
   u'NodeMeta': {u'consul-network-segment': u''},
   u'ServiceAddress': u'10.242.154.205',
   u'ServiceConnect': {},
   u'ServiceEnableTagOverride': False,
   u'ServiceID': u'f2468d6a-771d-4c84-a8a3-eb2e4f1f8628',
   u'ServiceKind': u'',
   u'ServiceMeta': {},
   u'ServiceName': u'namekox/ping',
   u'ServicePort': 80,
   u'ServiceProxy': {u'Expose': {}, u'MeshGateway': {}},
   u'ServiceTaggedAddresses': {u'lan_ipv4': {u'Address': u'10.242.154.205',
     u'Port': 80},
    u'wan_ipv4': {u'Address': u'10.242.154.205', u'Port': 80}},
   u'ServiceTags': [],
   u'ServiceWeights': {u'Passing': 1, u'Warning': 1},
   u'TaggedAddresses': {u'lan': u'127.0.0.1',
    u'lan_ipv4': u'127.0.0.1',
    u'wan': u'127.0.0.1',
    u'wan_ipv4': u'127.0.0.1'}}])
```
