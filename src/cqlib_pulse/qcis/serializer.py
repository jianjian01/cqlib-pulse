# (C) Copyright China Telecom Quantum Group 2026

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
