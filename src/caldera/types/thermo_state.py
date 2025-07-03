from pint import Quantity
from pydantic import BaseModel, field_validator

from ..errors import *
from ..types.scalars import (
    Pressure,
    SpecificEnthalpy,
    SpecificEntropy,
    SpecificInternalEnergy,
    SpecificVolume,
    Temperature,
)
from ..unit_converter import ensure_quantity

Parsable = Quantity | float | int | str


class ThermoState(BaseModel):
    temperature: Temperature
    pressure: Pressure
    specific_volume: SpecificVolume
    specific_internal_energy: SpecificInternalEnergy
    specific_enthalpy: SpecificEnthalpy
    specific_entropy: SpecificEntropy

    @field_validator("temperature", mode="before")
    def validate_temperature(self, v: Parsable) -> Temperature:
        v = ensure_quantity(v, "K")
        if v < 0.0:
            raise ValueBoundsError(v, 0, unit="K")
        return v

    @field_validator("pressure", mode="before")
    def validate_pressure(self, v: Parsable) -> Pressure:
        v = ensure_quantity(v, "Pa")
        if v < 0.0:
            raise ValueBoundsError(v, 0, unit="Pa")
        return v

    @field_validator("specific_volume", mode="before")
    def validate_specific_volume(self, v: Parsable) -> SpecificVolume:
        v = ensure_quantity(v, "m^3/kg")
        if v < 0.0:
            raise ValueBoundsError(v, 0, unit="m^3/kg")
        return v

    @field_validator("specific_internal_energy", mode="before")
    def validate_specific_internal_energy(self, v: Parsable) -> SpecificInternalEnergy:
        return ensure_quantity(v, "J/kg")

    @field_validator("specific_enthalpy", mode="before")
    def validate_specific_enthalpy(self, v: Parsable) -> SpecificEnthalpy:
        return ensure_quantity(v, "J/kg")

    @field_validator("specific_entropy", mode="before")
    def validate_specific_entropy(self, v: Parsable) -> SpecificEntropy:
        return ensure_quantity(v, "J/kg/K")
