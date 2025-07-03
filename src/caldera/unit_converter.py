from pint import Quantity, UnitRegistry
from pint.errors import DimensionalityError, UndefinedUnitError

from .errors import *

_UREG = UnitRegistry()


def ensure_quantity(value: str | float | Quantity, unit: str) -> float:
    if isinstance(value, str):
        try:
            value = _UREG.parse_expression(value, preprocessors=True)
        except (UndefinedUnitError, ValueError) as e:
            raise UnitParseError(str(value)) from e
    if isinstance(value, Quantity):
        try:
            return float(value.to(unit).magnitude)
        except DimensionalityError as e:
            raise InvalidUnitError(unit, str(value.units)) from e
    elif isinstance(value, float | int):
        return value
    else:
        raise TypeError
