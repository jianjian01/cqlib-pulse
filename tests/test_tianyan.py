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

from cqlib_pulse import CosineWaveform, PulseCircuit, TianyanExecutor


class FakeTask:
    def __init__(self):
        self.wait_options = None

    def wait(self, *, timeout_secs, poll_interval_secs):
        self.wait_options = (timeout_secs, poll_interval_secs)
        return [{"counts": {"0": 10}}]


class FakeBackend:
    def __init__(self):
        self.call = None
        self.task = FakeTask()

    def run(self, circuits, *, shots, **kwargs):
        self.call = (circuits, shots, kwargs)
        return self.task


def test_submit_and_wait_for_tianyan_result():
    circuit = PulseCircuit().pz(0, CosineWaveform(length=10, amplitude=0.2))
    backend = FakeBackend()

    execution = TianyanExecutor(backend).run(
        circuit,
        shots=200,
        timeout_secs=12,
        poll_interval_secs=0.5,
        priority="normal",
    )

    assert backend.call == (["PZ Q0 0 10 0.2 0"], 200, {"priority": "normal"})
    assert execution.task is backend.task
    assert execution.results == [{"counts": {"0": 10}}]
    assert backend.task.wait_options == (12, 0.5)
