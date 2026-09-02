# This code is part of cqlib.
#
# Copyright (C) 2026 China Telecom Quantum Group.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Operations stored by :class:`cqlib_pulse.PulseCircuit`."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..errors import PulseValidationError
from .instructions import PulseInstruction
from .targets import CouplerQubit, PulseTarget
from .waveforms import MAX_PULSE_LENGTH_NS, Number, validate_real


@dataclass(frozen=True, slots=True)
class PulseOperation:
    """A pulse instruction bound to one channel."""

    instruction: PulseInstruction
    target: PulseTarget

    def __post_init__(self) -> None:
        self.instruction.validate_target(self.target)

    @property
    def targets(self) -> tuple[PulseTarget, ...]:
        return (self.target,)


@dataclass(frozen=True, slots=True)
class StandardOperation:
    """A non-pulse QCIS operation retained in a mixed circuit."""

    opcode: str
    targets: tuple[PulseTarget, ...]
    parameters: tuple[Number, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "opcode", self.opcode.upper())
        object.__setattr__(self, "targets", tuple(self.targets))
        object.__setattr__(self, "parameters", tuple(self.parameters))
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", self.opcode):
            raise PulseValidationError(f"Invalid QCIS opcode: {self.opcode!r}")
        if not self.targets:
            raise PulseValidationError("A standard operation requires at least one target")
        for value in self.parameters:
            validate_real("operation parameter", value)
        if self.opcode == "I":
            if len(self.parameters) != 1 or not isinstance(self.parameters[0], int):
                raise PulseValidationError("I requires one integer length parameter")
            if not 0 <= self.parameters[0] <= MAX_PULSE_LENGTH_NS:
                raise PulseValidationError(f"I length must be in [0, {MAX_PULSE_LENGTH_NS}]")
        elif self.opcode == "RZ" and len(self.parameters) != 1:
            raise PulseValidationError("RZ requires one angle parameter")
        elif self.opcode in {"X2P", "M", "B"} and self.parameters:
            raise PulseValidationError(f"{self.opcode} does not accept parameters")
        if self.opcode in {"RZ", "X2P", "M"} and any(
            isinstance(target, CouplerQubit) for target in self.targets
        ):
            raise PulseValidationError(f"{self.opcode} requires data-qubit targets")


Operation = PulseOperation | StandardOperation


@dataclass(frozen=True, slots=True)
class ScheduledOperation:
    """An operation with its derived channel-relative time interval."""

    operation: Operation
    start_ns: int
    end_ns: int
