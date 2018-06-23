from app import what_ending


def test_what_ending():
    assert what_ending(0) == 'ok'
    assert what_ending(1) == 'ku'
    assert what_ending(2) == 'ky'
    assert what_ending(5) == 'ok'
