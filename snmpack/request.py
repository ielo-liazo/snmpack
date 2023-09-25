# -*- coding: utf-8 -*-

import random

from snmpack.objects import Message, PDUs, Version, Community, VarBindList, ObjectName, VarBind, ObjectValue

from snmpack.exceptions import SnmpackInvalidOid


class SNMPRequest:
    def __init__(self, rtype, root, oid=[], name=[], max_rep=10, **host):
        self.rtype = rtype
        self.root = root
        self.name = name
        self.host = host
        self.max_rep = max_rep
        self.oid = oid if not isinstance(oid, str) else [oid]
        self.pdu = PDUs(self.rtype)
        self.msg = Message()

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

        vb_list = VarBindList()

        for oid in self.oid:
            vb = VarBind()

            try:
                vb["name"] = ObjectName(oid)
            except ValueError:
                raise SnmpackInvalidOid

            vb["value"] = ObjectValue("empty")

            vb_list.append(vb)

        self.pdu.chosen["varbinds"] = vb_list

        return self.pdu

    def build(self, req_id=None) -> Message:
        self.msg["version"] = Version(self.host["version"])
        self.msg["community"] = Community(self.host["community"].encode())
        self.msg["data"] = self.build_pdu(req_id=req_id)

        return self.msg
