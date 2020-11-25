#! -*- coding: utf-8 -*-

# author: forcemain@163.com


from namekox_consul.core.proxy import ConsulProxy


class Consul(object):
    def __init__(self, config):
        self.config = config
        self.proxy = ConsulProxy(config)

    @classmethod
    def name(cls):
        return 'consul'
