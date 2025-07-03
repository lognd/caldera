from abc import ABC, abstractmethod

from ..types import PhaseState
from ..types.scalars import Pressure, Temperature


class PhaseDetectorABC(ABC):
    @abstractmethod
    def detect(self, T: Temperature, P: Pressure) -> PhaseState: ...
    @abstractmethod
    def is_within_bounds(self, T: Temperature, P: Pressure) -> bool: ...
