import pytest

from caldera.types.phase import InvalidPhaseError, PhaseFlag, PhaseState


@pytest.mark.parametrize(
    "flag",
    [
        PhaseFlag.SOLID,
        PhaseFlag.LIQUID,
        PhaseFlag.GAS,
        PhaseFlag.SUPERCRITICAL,
        PhaseFlag.EXOTIC,
        PhaseFlag.SATURATED,
        PhaseFlag.FUSED,
        PhaseFlag.SUBLIMATED,
        PhaseFlag.TRIPLE_POINT,
        PhaseFlag.SATURATED | PhaseFlag.CRITICAL,
        PhaseFlag.GAS | PhaseFlag.METASTABLE,
        PhaseFlag.LIQUID | PhaseFlag.METASTABLE,
        PhaseFlag.LIQUID | PhaseFlag.SPINODAL,
        PhaseFlag.NONE | PhaseFlag.METASTABLE,
    ],
    ids=lambda val: repr(val),
)
def test_valid_phase_flags(flag: PhaseFlag) -> None:
    state = PhaseState(flag=flag)
    assert state.flag == flag


@pytest.mark.parametrize(
    "flag",
    [
        PhaseFlag.GAS | PhaseFlag.LIQUID | PhaseFlag.SOLID | PhaseFlag.CRITICAL,
        PhaseFlag.SOLID | PhaseFlag.SPINODAL,
        PhaseFlag.TRIPLE_POINT | PhaseFlag.SPINODAL,
        PhaseFlag.LIQUID | PhaseFlag.SUPERCRITICAL,
        PhaseFlag.TRIPLE_POINT | PhaseFlag.CRITICAL,
        PhaseFlag.NONE,
        PhaseFlag.SOLID | PhaseFlag.CRITICAL,
    ],
    ids=lambda val: repr(val),
)
def test_invalid_phase_flags(flag: PhaseFlag) -> None:
    with pytest.raises(InvalidPhaseError):
        PhaseState(flag=flag)
