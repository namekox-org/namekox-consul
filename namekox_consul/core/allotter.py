#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import json
import time


from itertools import cycle
from namekox_core.core.generator import generator_md5
from namekox_consul.constants import DEFAULT_CONSUL_SERVICE_ROOT_PATH


class Allotter(object):
    def __init__(self, sdepd=None, ttl=36000):
        self.iters = {}
        self.sdepd = sdepd
        self.ttl = ttl

    def get(self, name):
        name = '{}/{}'.format(DEFAULT_CONSUL_SERVICE_ROOT_PATH, name)
        data = self.sdepd.instance.catalog.service(name)[1]
        if not data:
            self.iters.pop(name, None)
            raise KeyError(name)
        dmd5 = generator_md5(json.dumps(data))
        if name not in self.iters:
            self.iters[name] = [dmd5, cycle(data), time.time()]
        else:
            smd5, siter, stime = self.iters[name]
            if dmd5 != smd5 or time.time() - stime >= self.ttl:
                self.iters[name] = [dmd5, cycle(data), time.time()]
        return self.iters[name][1].next()

    def set(self, sdepd):
        self.iters = {}
        self.sdepd = sdepd
