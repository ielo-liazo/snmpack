# -*- coding: utf-8 -*-

from snmpack.objects import Message


class SNMPResponse:
    def __init__(self, data):
        self.parsed = Message.load(data)
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
