# -*- coding: utf-8 -*-

import snmp.objects as obj


class SNMPResponse(object):
    def __init__(self, data):
        self.parsed = obj.Message.load(data)
        self.pdu = self.parsed["data"].chosen

    @property
    def req_type(self):
        self.pdu["req_type"].native

    @property
    def req_id(self):
        return self.pdu["req_id"].native

    @property
    def last_varbind(self):
        return self.pdu["varbinds"][-1]
