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

"""Serialize pulse and standard operations as QCIS text."""

from __future__ import annotations

from collections.abc import Iterable

from ..core.operations import Operation, PulseOperation
from ..core.waveforms import Number


def format_number(value: Number) -> str:
    return str(value) if isinstance(value, int) else format(value, ".15g")


def operation_to_qcis(operation: Operation) -> str:
    if isinstance(operation, PulseOperation):
        parts = [
            operation.instruction.opcode,
            str(operation.target),
            *(format_number(value) for value in operation.instruction.parameters()),
        ]
    else:
        parts = [
            operation.opcode,
            *(str(target) for target in operation.targets),
            *(format_number(value) for value in operation.parameters),
        ]
    return " ".join(parts)


def dumps(operations: Iterable[Operation]) -> str:
    return "\n".join(operation_to_qcis(operation) for operation in operations)
