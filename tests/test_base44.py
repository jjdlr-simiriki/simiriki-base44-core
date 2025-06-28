import base44


def test_roundtrip_leading_zeros():
    data = b"\x00\x00\x01"
    assert base44.decode(base44.encode(data)) == data
