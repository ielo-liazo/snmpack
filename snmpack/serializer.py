# -*- coding: utf-8 -*-

import json
import binascii

import ipaddress


class SNMPJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ipaddress.IPv4Address):
            return o.exploded

        return super().default(o)
