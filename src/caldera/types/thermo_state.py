from pydantic import BaseModel, field_validator

from caldera.types.scalars import Temperature, Pressure, SpecificVolume, SpecificInternalEnergy, SpecificEnthalpy, SpecificEntropy
from caldera.unit_converter import ensure_quantity

class ThermoState(BaseModel):
    temperature: Temperature
    pressure: Pressure
    specific_volume: SpecificVolume
    specific_internal_energy: SpecificInternalEnergy
    specific_enthalpy: SpecificEnthalpy
    specific_entropy: SpecificEntropy

    @field_validator("temperature", mode="before")
    def validate_temperature(cls, v):
        v = ensure_quantity(v, 'K')
        if v < 0.0: raise ValueError("Temperature must be above 0 K.")
        return v

    @field_validator("pressure", mode="before")
    def validate_pressure(cls, v):
        v = ensure_quantity(v, 'Pa')
        if v < 0.0: raise ValueError("Pressure must be above 0 Pa.")

    @field_validator("specific_volume", mode="before")
    def validate_specific_volume(cls, v):
        v = ensure_quantity(v, 'm^3/kg')
        if v < 0.0: raise ValueError("Specific volume must be above 0 m^3/kg.")

    @field_validator("specific_internal_energy", mode="before")
    def validate_specific_internal_energy(cls, v):
        return ensure_quantity(v, 'J/kg')

    @field_validator("specific_enthalpy", mode="before")
    def validate_specific_enthalpy(cls, v):
        return ensure_quantity(v, 'J/kg')

    @field_validator("specific_entropy", mode="before")
    def validate_specific_entropy(cls, v):
        return ensure_quantity(v, 'J/kg/K')