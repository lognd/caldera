from pint import Quantity, UnitRegistry

_UREG = UnitRegistry()
def ensure_quantity(value: str | float | Quantity, unit: str) -> float:
    if isinstance(value, str):
        try: value = _UREG.parse_expression(value, preprocessors=True)
        except Exception: raise ValueError(f'Could not parse string, "{value}", into quantity.')
    if isinstance(value, Quantity):
        try: return value.to(unit).magnitude
        except Exception: raise ValueError(f"Expected a quantity in `{unit}`, got `{value.units}`.")
    elif isinstance(value, float | int): return value
    else: raise TypeError(f"Expected float, str, or Quantity, got `{type(value)}`.")
