# -*- coding: utf-8 -*-

import binascii
import ipaddress

import asn1crypto.core as asn1

from exceptions import SnmpackNoSuchInstance, SnmpackNoSuchObject, SnmpackEndOfMib


class Integer(asn1.Integer):
    def __unicode__(self):
        return "{}".format(self.contents)


class Version(Integer):
    _map = {
        0: "1",
        1: "2c"
    }

    def __unicode__(self):
        return str(self.native)


class Community(asn1.OctetString):
    def __unicode__(self):
        return str(self.native)


class RequestID(Integer):
    def __unicode__(self):
        return str(self.native)

    def __eq__(self, other):
        return self.native == other

    def __hash__(self):
        return hash(self.native)


class ErrorStatus(Integer):
    _map = {
        0: "success",
        1: "too big",
        2: "no such name",
        3: "bad value",
        4: "read only",
        5: "gen err"
    }


class ErrorIndex(Integer):
    pass


class TimeTicks(Integer):
    class_ = 1
    tag = 3


class HexString(asn1.BitString):
    class_ = 1
    tag = 2

    @property
    def native(self):
        return binascii.hexlify(self.contents)


class ObjectName(asn1.ObjectIdentifier):
    pass


class Counter64(Integer):
    class_ = 1
    tag = 6


class Counter32(Integer):
    class_ = 1
    tag = 1


class Gauge(Integer):
    class_ = 1
    tag = 2


class Opaque(asn1.OctetString):
    class_ = 1
    tag = 4


class IpAddress(asn1.OctetString):
    class_ = 1
    tag = 0

    @property
    def native(self):
        return ipaddress.ip_address(self.contents)


class String(asn1.OctetString):
    @property
    def native(self):
        # FIXME il faut corriger le tag de BitString
        try:
            return self.contents.decode("utf-8")
        except UnicodeDecodeError:
            return binascii.hexlify(self.contents).decode("utf-8")

    def __unicode__(self):
        return self.native


class NoSuchObject(asn1.Integer):
    @property
    def native(self):
        raise SnmpackNoSuchObject("no such object")

    def __unicode__(self):
        return str(self.__class__)


class NoSuchInstance(asn1.Integer):
    @property
    def native(self):
        raise SnmpackNoSuchInstance("no such instance")

    def __unicode__(self):
        return str(self.__class__)


class EndOfMib(asn1.Integer):
    @property
    def native(self):
        raise SnmpackEndOfMib("end of mib")

    def __unicode__(self):
        return str(self.__class__)


class ObjectValue(asn1.Choice):
    _alternatives = [
        ("integer", Integer),
        ("string", String),
        ("object", asn1.ObjectIdentifier),
        ("timetick", TimeTicks),
        ("hexString", HexString),
        ("counter64", Counter64),
        ("counter32", Counter32),
        ("gauge", Gauge),
        ("opaque", Opaque),
        ("ipaddress", IpAddress),
        ("empty", asn1.Null),
        ("noSuchObject", NoSuchObject, {"tag_type": "implicit", "tag": 0}),
        ("noSuchInstance", NoSuchInstance, {"tag_type": "implicit", "tag": 1}),
        ("endOfMib", EndOfMib, {"tag_type": "implicit", "tag": 2})
    ]

    def __unicode__(self):
        return str(self.__class__)


class VarBind(asn1.Sequence):
    _fields = [
        ("name", ObjectName),
        ("value", ObjectValue)
    ]

    def __unicode__(self):
        return str(self.native)


class VarBindList(asn1.SequenceOf):
    _child_spec = VarBind

    def __unicode__(self):
        res = []
        for vb in self:
            res.append(vb.__unicode__())

        return "".join(res)

class BasePDU(asn1.Sequence):
    _fields = [
        ("req_id", RequestID),
        ("error_status", ErrorStatus),
        ("error_index", ErrorIndex),
        ("varbinds", VarBindList)
    ]


class GetRequestPDU(BasePDU):
    pass


class GetNextRequestPDU(BasePDU):
    pass


class GetResponsePDU(BasePDU):
    pass


class SetRequestPDU(BasePDU):
    pass


class BulkNextRequestPDU(BasePDU):
    _fields = [
        ("req_id", RequestID),
        ("non_repeaters", Integer),
        ("max_repetitions", Integer),
        ("varbinds", VarBindList)
    ]


class PDUs(asn1.Choice):
    _alternatives = [
        ("get_request", GetRequestPDU, {"tag_type": "implicit", "tag": 0}),
        ("get_next_request", GetNextRequestPDU, {"tag_type": "implicit", "tag": 1}),
        ("get_response", GetResponsePDU, {"tag_type": "implicit", "tag": 2}),
        ("set_request", SetRequestPDU, {"tag_type": "implicit", "tag": 3}),
        ("bulk_next_request", BulkNextRequestPDU, {"tag_type": "implicit", "tag": 5})
    ]

    def __unicode__(self):
        return str(self.native)


class Message(asn1.Sequence):
    _fields = [
        ("version", Version),
        ("community", Community),
        ("data", PDUs)
    ]

    def __unicode__(self):
        return "[%d] [%s] [%s]" % (self["version"], self["community"], self["data"].__unicode__())
