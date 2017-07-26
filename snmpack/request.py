# -*- coding: utf-8 -*-

import random

import snmpack.snmpack.objects as obj

from snmpack.snmpack.exceptions import SnmpackInvalidOid


class SNMPRequest(object):
    def __init__(self, rtype, root, oid=[], name=[], max_rep=10, **host):
        self.rtype = rtype
        self.root = root
        self.name = name
        self.host = host
        self.max_rep = max_rep
        self.oid = oid if not isinstance(oid, str) else [oid]
        self.pdu = obj.PDUs(self.rtype)
        self.msg = obj.Message()

    @property
    def req_id(self):
        return self.pdu.chosen["req_id"]

    @property
    def timeout(self):
        return self.host["timeout"]

    def find_name(self, vb_oid):
        for oid, measurement in self.name.items():
            if vb_oid.startswith("%s.%s" % (self.root, oid)):
                return (oid, measurement)

        raise KeyError

    def build_pdu(self, req_id=None):
        if req_id is None:
            self.pdu.chosen["req_id"] = random.randint(1, 100000000)
        else:
            self.pdu.chosen["req_id"] = req_id

        if self.rtype == "bulk_next_request":
            self.pdu.chosen["non_repeaters"] = 0
            self.pdu.chosen["max_repetitions"] = self.max_rep
        else:
            self.pdu.chosen["error_status"] = 0
            self.pdu.chosen["error_index"] = 0

        vb_list = obj.VarBindList()

        for oid in self.oid:
            vb = obj.VarBind()

            try:
                vb["name"] = obj.ObjectName(oid)
            except ValueError as e:
                raise SnmpackInvalidOid

            vb["value"] = obj.ObjectValue("empty")

            vb_list.append(vb)

        self.pdu.chosen["varbinds"] = vb_list

        return self.pdu

    def build(self, req_id=None):
        self.msg["version"] = obj.Version(self.host["version"])
        self.msg["community"] = obj.Community(self.host["community"].encode())
        self.msg["data"] = self.build_pdu(req_id=req_id)

        return self.msg
