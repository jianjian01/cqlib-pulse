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

"""Optional adapter for task execution through ``cqlib-tianyan``."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from ..core.circuit import PulseCircuit
from ..errors import TianyanIntegrationError


@runtime_checkable
class TianyanTask(Protocol):
    """The small part of a cqlib-tianyan task used by this package."""

    def wait(self, *, timeout_secs: float, poll_interval_secs: float) -> Any: ...


@runtime_checkable
class TianyanBackend(Protocol):
    """Backend interface used by the executor and test doubles."""

    def run(self, circuits: list[str], *, shots: int, **kwargs: Any) -> TianyanTask: ...


@dataclass(slots=True)
class PulseExecution:
    """A submitted cloud task and, after waiting, its returned results."""

    task: TianyanTask
    results: Any = None


class TianyanExecutor:
    """Submit pulse QCIS to a backend provided by cqlib-tianyan."""

    def __init__(self, backend: TianyanBackend) -> None:
        self.backend = backend

    @classmethod
    def login(cls, api_key: str, machine_name: str) -> "TianyanExecutor":
        """Log in with cqlib-tianyan and select a backend lazily.

        Keeping this import lazy lets the core pulse data model remain usable
        without installing cloud dependencies.
        """

        try:
            from cqlib_tianyan import TianyanPlatform  # type: ignore[import-not-found]
        except ImportError as exc:
            raise TianyanIntegrationError(
                "Install the Tianyan extra first: pip install 'cqlib-pulse[tianyan]'"
            ) from exc

        try:
            platform = TianyanPlatform.login(api_key)
            backend = platform.get_backend(machine_name)
        except (AttributeError, TypeError) as exc:
            raise TianyanIntegrationError(
                "Installed cqlib-tianyan does not provide "
                "TianyanPlatform.login(...).get_backend(...)"
            ) from exc
        return cls(backend)

    def submit(
        self,
        circuit: PulseCircuit | str,
        *,
        shots: int = 1_000,
        **run_options: Any,
    ) -> PulseExecution:
        """Submit one circuit and return immediately with its task handle."""

        if isinstance(shots, bool) or not isinstance(shots, int) or shots <= 0:
            raise ValueError("shots must be a positive integer")
        qcis = circuit.to_qcis() if isinstance(circuit, PulseCircuit) else circuit
        if not isinstance(qcis, str) or not qcis.strip():
            raise ValueError("circuit must contain non-empty QCIS")
        task = self.backend.run([qcis], shots=shots, **run_options)
        return PulseExecution(task=task)

    def run(
        self,
        circuit: PulseCircuit | str,
        *,
        shots: int = 1_000,
        timeout_secs: float = 3_600,
        poll_interval_secs: float = 10,
        **run_options: Any,
    ) -> PulseExecution:
        """Submit a circuit, wait for completion and retain the task handle."""

        execution = self.submit(circuit, shots=shots, **run_options)
        execution.results = execution.task.wait(
            timeout_secs=timeout_secs,
            poll_interval_secs=poll_interval_secs,
        )
        return execution
