from __future__ import annotations

from enum import IntFlag

from pydantic import BaseModel, Field, field_validator
from ..errors import *

class PhaseState(BaseModel):
    flag: PhaseFlag = Field(..., description="Bitmask representing the phase and modifiers...")

    @field_validator("flag")
    def check_phase_flag(self, v: PhaseFlag) -> PhaseFlag:
        if not validate_phase_flag(v):
            raise InvalidPhaseError(v)
        return v


def validate_phase_flag(phase_flag: PhaseFlag) -> bool:
    if phase_flag <= 0 or phase_flag > 0xFF:
        return False
    base = phase_flag & PhaseFlag.BASE
    modifier = phase_flag & PhaseFlag.MODIFIER

    if modifier not in {
        PhaseFlag.NONE,
        PhaseFlag.CRITICAL,
        PhaseFlag.METASTABLE,
        PhaseFlag.SPINODAL,
    }:
        return False

    if modifier & PhaseFlag.CRITICAL:
        return base in {PhaseFlag.NONE, PhaseFlag.SATURATED}

    if modifier & PhaseFlag.METASTABLE:
        return base in {PhaseFlag.NONE, PhaseFlag.GAS, PhaseFlag.LIQUID}

    if modifier & PhaseFlag.SPINODAL:
        return base in {PhaseFlag.NONE, PhaseFlag.LIQUID, PhaseFlag.GAS}

    return base in {
        PhaseFlag.SOLID,
        PhaseFlag.LIQUID,
        PhaseFlag.GAS,
        PhaseFlag.SUPERCRITICAL,
        PhaseFlag.EXOTIC,
        PhaseFlag.SATURATED,
        PhaseFlag.SUBLIMATED,
        PhaseFlag.FUSED,
        PhaseFlag.TRIPLE_POINT,
    }


class PhaseFlag(IntFlag):
    # Flag regions
    BASE = 0b00001111
    MODIFIER = 0b11110000

    NONE = 0b00000000

    # BASIC STATES
    SOLID = 0b00000001
    LIQUID = 0b00000010
    GAS = 0b00000100
    SUPERCRITICAL = 0b00001000

    EXOTIC = 0b00001111  # Reserved for phases outside of normal thermo.

    # SATURATED STATES
    SATURATED = LIQUID | GAS
    FUSED = SOLID | LIQUID
    SUBLIMATED = SOLID | GAS

    TRIPLE_POINT = SOLID | LIQUID | GAS

    # MUTUALLY-EXCLUSIVE FLAGS
    CRITICAL = 0b00010000
    METASTABLE = 0b00100000
    SPINODAL = 0b01000000
