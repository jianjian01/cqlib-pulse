import pytest

from cqlib_pulse import (
    CosineWaveform,
    FlattopWaveform,
    NumericWaveform,
    PulseValidationError,
    SlepianWaveform,
    Waveform,
    WaveformType,
)


@pytest.mark.parametrize(
    "waveform",
    [
        CosineWaveform(length=10, amplitude=-0.2),
        FlattopWaveform(length=10, amplitude=0.2, edge=2.5),
        SlepianWaveform(
            length=10,
            amplitude=0.2,
            thf=-0.1,
            thi=0.2,
            lam2=0.3,
            lam3=1.0,
        ),
        NumericWaveform(length=10, amplitude=0.2, data_list=(-0.1, 0.2, 1.3)),
    ],
)
def test_waveform_round_trip(waveform):
    restored = Waveform.load(waveform.data)
    assert restored == waveform
    assert str(restored) == str(waveform)


def test_numeric_waveform_protocol_identifier_is_minus_one():
    waveform = Waveform.create(
        WaveformType.NUMERIC,
        length=20,
        amplitude=0.5,
        samples=(0.1, 0.2, 0.3),
    )
    assert isinstance(waveform, NumericWaveform)
    assert waveform.data == [-1, 20, 0.5, 0.1, 0.2, 0.3]


@pytest.mark.parametrize(
    "waveform",
    [
        lambda: CosineWaveform(length=-1, amplitude=0.2),
        lambda: CosineWaveform(length=49_985, amplitude=0.2),
        lambda: SlepianWaveform(
            length=10, amplitude=0.2, thf=1.1, thi=0, lam2=0, lam3=0
        ),
    ],
)
def test_waveform_validation(waveform):
    with pytest.raises(PulseValidationError):
        waveform()


def test_pxy_specific_values_are_not_waveform_fields():
    with pytest.raises(TypeError):
        CosineWaveform(length=10, amplitude=0.2, phase=0.0)  # type: ignore[call-arg]
