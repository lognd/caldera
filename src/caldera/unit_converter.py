import re

from pint import Quantity
from pint.errors import DimensionalityError, UndefinedUnitError

from .errors import *

_QUANTITY_REGEX = re.compile(r"^\s*(?P<value>[-+]?[\d.]+(?:e[-+]?\d+)?)\s*(?P<unit>.+)$")


def ensure_quantity(value: str | float | Quantity, unit: str) -> float:
    if isinstance(value, str):
        try:
            groups = _QUANTITY_REGEX.match(value)
            if not groups:
                raise UnitParseError(str(value))

            value_str = groups.group("value")
            unit_str = groups.group("unit").strip()
            value = Quantity(float(value_str), unit_str)
        except (UndefinedUnitError, ValueError) as e:
            raise UnitParseError(str(value)) from e
    if isinstance(value, Quantity):
        try:
            return float(value.to(unit).magnitude)
        except DimensionalityError as e:
            raise UnitTypeError(unit, str(value.units)) from e
    elif isinstance(value, float | int):
        return value
    else:
        raise TypeError
