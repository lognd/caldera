from __future__ import annotations
from enum import IntFlag
from pydantic import BaseModel, field_validator, Field

class PhaseState(BaseModel):
    flag: PhaseFlag = Field(..., description="Bitmask representing the phase and modifiers...")

    @field_validator("flag")
    def check_phase_flag(cls, v):
        if not validate_phase_flag(v):
            raise ValueError(f"Invalid PhaseFlag combination: {v}")
        return v

def validate_phase_flag(phase_flag: PhaseFlag) -> bool:
    if phase_flag <= 0 or phase_flag > 255: return False
    base = phase_flag & PhaseFlag.BASE
    modifier = phase_flag & PhaseFlag.MODIFIER

    if modifier not in {PhaseFlag.NONE, PhaseFlag.CRITICAL, PhaseFlag.METASTABLE, PhaseFlag.SPINODAL}:
        return False

    elif modifier & PhaseFlag.CRITICAL:
        if base == PhaseFlag.NONE: return True  # shortcut
        elif base == PhaseFlag.SATURATED: return True  # critical is in saturated region.
        return False  # all other combinations are invalid.

    elif modifier & PhaseFlag.METASTABLE:
        if base == PhaseFlag.NONE: return True
        elif base == PhaseFlag.GAS: return True
        elif base == PhaseFlag.LIQUID: return True
        elif base == PhaseFlag.SOLID: return False  # metastable solids should be exotic.
        return False

    elif modifier & PhaseFlag.SPINODAL:
        if base == PhaseFlag.NONE: return True
        elif base == PhaseFlag.LIQUID: return True
        elif base == PhaseFlag.GAS: return True
        return False

    else:
        if base == PhaseFlag.NONE: return False

        elif base == PhaseFlag.SOLID: return True
        elif base == PhaseFlag.LIQUID: return True
        elif base == PhaseFlag.GAS: return True

        elif base == PhaseFlag.SATURATED: return True
        elif base == PhaseFlag.FUSED: return True
        elif base == PhaseFlag.SUBLIMATED: return True

        elif base == PhaseFlag.SUPERCRITICAL: return True
        elif base == PhaseFlag.TRIPLE_POINT: return True
        elif base == PhaseFlag.EXOTIC: return True

        return False

class PhaseFlag(IntFlag):
    # Flag regions
    BASE          = 0b00001111
    MODIFIER      = 0b11110000

    NONE          = 0b00000000

    # BASIC STATES
    SOLID         = 0b00000001
    LIQUID        = 0b00000010
    GAS           = 0b00000100
    SUPERCRITICAL = 0b00001000

    EXOTIC        = 0b00001111  # Reserved for phases outside of normal thermo.

    # SATURATED STATES
    SATURATED     = LIQUID | GAS
    FUSED         = SOLID | LIQUID
    SUBLIMATED    = SOLID | GAS

    TRIPLE_POINT  = SOLID | LIQUID | GAS

    # MUTUALLY-EXCLUSIVE FLAGS
    CRITICAL      = 0b00010000
    METASTABLE    = 0b00100000
    SPINODAL      = 0b01000000




