import pytest
from cqlib import Qubit as CqlibQubit

from cqlib_pulse import (
    CosineWaveform,
    CouplerQubit,
    PulseCircuit,
    PulseValidationError,
    QCISParseError,
    Qubit,
    StandardOperation,
)


def test_build_and_round_trip_protocol_qcis():
    circuit = PulseCircuit(qubits=[0], coupler_qubits=[107])
    circuit.pxy(
        0,
        CosineWaveform(length=40, amplitude=0.2),
        frequency=5e9,
        phase=0.1,
        drag_alpha=-0.2,
    )
    circuit.pz(
        CouplerQubit(107),
        CosineWaveform(length=20, amplitude=-0.1),
        call_mapper=True,
    )
    circuit.g(107, 100, -3_000_000.5)

    expected = (
        "PXY Q0 0 40 0.2 5000000000 0.1 -0.2\n"
        "PZ G107 0 20 -0.1 1\n"
        "G G107 100 -3000000.5"
    )
    assert circuit.to_qcis() == expected
    assert PulseCircuit.load(expected).to_qcis() == expected
    assert circuit.qubits == (Qubit(0),)
    assert circuit.coupler_qubits == (CouplerQubit(107),)


def test_mixed_standard_and_pulse_qcis_round_trip():
    qcis = (
        "X2P Q0\n"
        "RZ Q0 1.25\n"
        "I Q0 20\n"
        "PZ0 Q0 0 10 0.2 0\n"
        "B Q0 Q1\n"
        "M Q0"
    )
    circuit = PulseCircuit.from_qcis(qcis)
    assert circuit.to_qcis() == qcis
    assert isinstance(circuit[0], StandardOperation)


def test_pz0_does_not_advance_channel_time_but_delay_does():
    circuit = PulseCircuit()
    circuit.pz0(0, CosineWaveform(length=30, amplitude=0.2))
    circuit.delay(0, 20)
    circuit.pz(0, CosineWaveform(length=10, amplitude=0.1))

    assert [(item.start_ns, item.end_ns) for item in circuit.schedule()] == [
        (0, 30),
        (0, 20),
        (20, 30),
    ]
    assert circuit.channel_times == {Qubit(0): 30}


def test_public_qubit_is_the_official_cqlib_type():
    assert Qubit is CqlibQubit
    circuit = PulseCircuit().pz(
        CqlibQubit(3),
        CosineWaveform(length=10, amplitude=0.2),
    )
    assert circuit.to_qcis() == "PZ Q3 0 10 0.2 0"


def test_parse_ignores_comments_and_blank_lines():
    circuit = PulseCircuit.from_qcis("# demo\nPZ Q2 0 10 0.2 1 // pulse\n")
    assert circuit.to_qcis() == "PZ Q2 0 10 0.2 1"


def test_target_rules_are_enforced():
    waveform = CosineWaveform(length=10, amplitude=0.2)
    with pytest.raises(PulseValidationError, match="data qubit"):
        PulseCircuit().pxy(CouplerQubit(1), waveform, frequency=5e9)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "qcis",
    [
        "G Q0 10 20",
        "PZ Q0 99 10 0.2 0",
        "PXY Q0 0 10 0.2",
        "I Q0 10 extra",
    ],
)
def test_invalid_qcis_reports_line(qcis):
    with pytest.raises(QCISParseError, match="Line 1"):
        PulseCircuit.from_qcis(qcis)
