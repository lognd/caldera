class CalderaError(Exception):
    """Base class for exceptions raised by Caldera."""

class ValueBoundsError(CalderaError):
    """Raised when a value is outside a defined range."""

    def __init__(self, value: float | int, min_: float | int = None, max_: float | int = None, unit: str = None):
        if unit is None:
            unit_text = ""
        else:
            unit_text = f" {unit}"
        if min_ is not None and max_ is not None:
            super().__init__(f'Input value, `{value}{unit_text}`, must be between `{min_}{unit_text}` and `{max_}{unit_text}`.')
        elif min_ is not None:
            super().__init__(f'Input value, `{value}{unit_text}`, must be greater than `{min_}{unit_text}`.')
        elif max_ is not None:
            super().__init__(f'Input value, `{value}{unit_text}`, must be less than `{max_}{unit_text}`.')
        else:
            super().__init__(f'Input value, `{value}{unit_text}`, is not in a valid range.')

class UnitParseError(CalderaError):
    """Raised when a pint cannot parse a string."""

    def __init__(self, value: str):
        super().__init__(f'Could not parse string, "{value}", into quantity.')

class InvalidUnitError(CalderaError):
    """Raised when a pint.Quantity has the wrong units."""

    def __init__(self, expected: str, actual: str):
        super().__init__(f"Expected a quantity in `{expected}`, got `{actual}`.")

class InvalidPhaseError(CalderaError):
    """Raised when an invalid PhaseFlag is made or produced."""

    def __init__(self, flag: object):
        super().__init__(f"`{flag.__repr__()}` is not a valid phase flag.")
