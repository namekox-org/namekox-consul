#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


from consul import Consul
from namekox_core.core.friendly import AsLazyProperty
from namekox_consul.constants import CONSUL_CONFIG_KEY


class ConsulProxy(object):
    def __init__(self, config, **options):
        self.config = config
        self.options = options

    @AsLazyProperty
    def configs(self):
        return self.config.get(CONSUL_CONFIG_KEY, {})

    def __call__(self, dbname, **options):
        self.options.update(options)
        config = self.configs.get(dbname, {})
        config.update(self.options)
        return Consul(**config)
