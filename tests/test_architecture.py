def test_layered_imports_and_top_level_api_are_available():
    from cqlib_pulse import PulseCircuit as PublicCircuit
    from cqlib_pulse.cloud import TianyanExecutor
    from cqlib_pulse.core import PulseCircuit
    from cqlib_pulse.qcis import dumps, loads

    assert PublicCircuit is PulseCircuit
    assert PulseCircuit.__module__ == "cqlib_pulse.core.circuit"
    assert TianyanExecutor.__module__ == "cqlib_pulse.cloud.executor"
    assert dumps(loads("X2P Q0")) == "X2P Q0"
