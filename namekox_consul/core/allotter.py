#! -*- coding: utf-8 -*-

# author: forcemain@163.com


import random


class Allotter(object):
    def __init__(self, sdepd=None):
        self.sdepd = sdepd

    def get(self, name):
        name = self.sdepd.gen_serv_name(name)
        index, data = self.sdepd.instance.health.service(name, passing=True)
        if not data: raise KeyError(name)
        data = random.choice(data)
        return {'address': data['Service']['Address'], 'port': data['Service']['Port']}

    def set(self, sdepd):
        self.sdepd = sdepd
