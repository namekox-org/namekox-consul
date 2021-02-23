#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import six
import consul
import socket


from namekox_consul.constants import CONSUL_CONFIG_KEY
from namekox_core.core.generator import generator_uuid
from namekox_core.core.service.dependency import Dependency
from namekox_core.core.friendly import AsLazyProperty, ignore_exception


class ConsulHelper(Dependency):
    def __init__(self, dbname, serverid=None, watching=None, allotter=None, coptions=None, roptions=None):
        self.instance = None
        self.dbname = dbname
        self.watching = watching
        self.allotter = allotter
        self.coptions = coptions or {}
        self.roptions = roptions or {}
        self.serverid = serverid or generator_uuid()
        super(ConsulHelper, self).__init__(dbname, serverid, watching, allotter, coptions, roptions)

    @AsLazyProperty
    def configs(self):
        return self.container.config.get(CONSUL_CONFIG_KEY, {})

    @staticmethod
    def get_host_byname():
        name = socket.gethostname()
        return ignore_exception(socket.gethostbyname)(name)

    def gen_serv_name(self, name):
        return '{}/{}'.format(self.watching, name)

    def setup_register(self):
        r_options = self.roptions.copy()
        host_addr = self.get_host_byname()
        serv_name = self.gen_serv_name(self.container.service_cls.name)
        r_options.setdefault('port', 80)
        r_options.setdefault('service_id', self.serverid)
        r_options.setdefault('address', host_addr or '127.0.0.1')
        check = consul.Check().tcp(r_options['address'], r_options['port'], '5s', '10s', '10s')
        r_options.setdefault('check', check)
        self.instance.agent.service.register(serv_name, **r_options)

    def setup_allotter(self):
        self.allotter.set(self)

    def setup(self):
        config = self.configs.get(self.dbname, {}).copy()
        [config.update({k: v}) for k, v in six.iteritems(self.coptions)]
        self.instance = consul.Consul(**config)
        self.coptions = config

    def start(self):
        self.watching and self.setup_register()
        self.allotter and self.setup_allotter()

    def stop(self):
        self.instance and ignore_exception(self.instance.agent.service.deregister)(self.serverid)
