# (C) Copyright China Telecom Quantum Group 2026

"""Qubit target value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from cqlib import Qubit

from ..errors import PulseValidationError


@dataclass(frozen=True, slots=True, order=True)
class CouplerQubit:
    """A coupling channel, serialized as ``G<index>`` in QCIS."""

    index: int

    def __post_init__(self) -> None:
        if isinstance(self.index, bool) or not isinstance(self.index, int) or self.index < 0:
            raise PulseValidationError("CouplerQubit index must be a non-negative integer")

    def __str__(self) -> str:
        return f"G{self.index}"


PulseTarget: TypeAlias = Qubit | CouplerQubit


def parse_target(value: str) -> PulseTarget:
    """Parse a QCIS target token such as ``Q3`` or ``G107``."""

    if len(value) < 2 or value[0] not in {"Q", "G"} or not value[1:].isdigit():
        raise PulseValidationError(f"Invalid pulse target: {value!r}")
    cls = Qubit if value[0] == "Q" else CouplerQubit
    return cls(int(value[1:]))
