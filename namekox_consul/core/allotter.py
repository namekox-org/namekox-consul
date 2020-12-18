#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import random


from namekox_consul.exceptions import RegServiceNotFound


class Allotter(object):
    def __init__(self, sdepd=None):
        self.sdepd = sdepd

    def _raise(self, exc, errs=None):
        raise (exc if errs is None else exc(errs))

    def get(self, name):
        name = self.sdepd.gen_serv_name(name)
        data = self.sdepd.instance.health.service(name, passing=True)[-1]
        data or self._raise(RegServiceNotFound, name)
        data = random.choice(data)
        port = data['Service']['Port']
        host = data['Service']['Address']
        return {'address': host, 'port': port}

    def set(self, sdepd):
        self.sdepd = sdepd
