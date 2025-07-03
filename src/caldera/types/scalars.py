from typing import Annotated

from pydantic import Field

Temperature = Annotated[float, Field("Temperature in K (kelvin)")]
Pressure = Annotated[float, Field("Pressure in Pa (pascals)")]

SpecificVolume = Annotated[float, Field("Specific Volume in m^3/kg")]
SpecificEnthalpy = Annotated[float, Field("Specific Enthalpy in J/kg")]
SpecificInternalEnergy = Annotated[float, Field("Specific Internal Energy in J/kg")]
SpecificEntropy = Annotated[float, Field("Specific Entropy in J/(kg K)")]
