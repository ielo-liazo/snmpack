import pytest
from snmpack.request import SNMPRequest


def test_wrong_alternative():
    with pytest.raises(ValueError) as e:
        SNMPRequest("foo", "bar")
    assert (
        e.value.args[0]
        == 'The name specified, "foo", is not a valid alternative for snmpack.objects.PDUs\n    while constructing snmpack.objects.PDUs'
    )


def test_simple_pdus():
    s = SNMPRequest("get_request", "1.3.6.1.2.1.31.1.1.1")
