from caldera import _hello_world as ping


def test_sanity_check() -> None:
    assert True
    assert ping() == '"Hello" from caldera!'
