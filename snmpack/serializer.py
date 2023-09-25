# -*- coding: utf-8 -*-

import json
from datetime import date, datetime
import ipaddress


class SNMPJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return super().default(0)
        except Exception:
            match o:
                case ipaddress.IPv4Address():
                    return o.exploded
                case ipaddress.IPv6Address():
                    return o.exploded
                case datetime():
                    return o.isoformat()
                case date():
                    return o.isoformat()
                case _:
                    return str(o)
