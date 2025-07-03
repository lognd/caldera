import pytest
from pint import Quantity

from caldera.errors import UnitParseError, UnitTypeError
from caldera.unit_converter import ensure_quantity


def test_float_passthrough() -> None:
    assert ensure_quantity(300.0, "kelvin") == 300.0
    assert ensure_quantity(100, "kelvin") == 100.0


def test_valid_quantity_conversion() -> None:
    q = Quantity(1, "bar")
    result = ensure_quantity(q, "pascal")
    assert pytest.approx(result, rel=1e-6) == 1e5


def test_valid_string_expression() -> None:
    assert pytest.approx(ensure_quantity("1000 mbar", "pascal")) == 100000.0
    assert pytest.approx(ensure_quantity("25 degC", "kelvin")) == 298.15


def test_invalid_unit_in_string() -> None:
    with pytest.raises(UnitParseError):
        ensure_quantity("15 hawk", "kelvin")


def test_incorrect_quantity_units() -> None:
    q = Quantity(5, "second")
    with pytest.raises(UnitTypeError):
        ensure_quantity(q, "kelvin")


def test_malformed_type_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        ensure_quantity(None, "kelvin")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        ensure_quantity([], "kelvin")  # type: ignore[arg-type]
