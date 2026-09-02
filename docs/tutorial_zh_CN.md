<!--
This code is part of cqlib.

Copyright (C) 2026 China Telecom Quantum Group.

This code is licensed under the Apache License, Version 2.0. You may
obtain a copy of this license in the LICENSE file in the root directory
of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.

Any modifications or derivative works of this code must retain this
copyright notice, and modified files need to carry a notice indicating
that they have been altered from the originals.
-->

# cqlib-pulse 中文教程

## 安装

在项目根目录执行：

```bash
python -m pip install -e .
```

天衍云端功能使用可选依赖：

```bash
python -m pip install -e '.[tianyan]'
```

## 构建脉冲线路

```python
from cqlib_pulse import CosineWaveform, CouplerQubit, PulseCircuit

circuit = PulseCircuit()
circuit.pxy(
    1,
    CosineWaveform(length=40, amplitude=0.2),
    frequency=5e9,
    phase=0.0,
    drag_alpha=1.0,
)
circuit.pz(
    CouplerQubit(107),
    CosineWaveform(length=20, amplitude=-0.1),
    call_mapper=True,
)
circuit.g(107, length=100, coupling_strength=-3_000_000)
circuit.delay(1, length=20)
circuit.measure(1)
```

## 转换和解析 QCIS

```python
qcis = circuit.to_qcis()
print(qcis)

restored = PulseCircuit.from_qcis(qcis)
print(restored.schedule())
print(restored.channel_times)
```

`schedule()` 返回各操作的起止时间，`channel_times` 返回各通道的最终时刻。

## 提交到天衍平台

```python
from cqlib_pulse import TianyanExecutor

executor = TianyanExecutor.login(
    api_key="your-api-key",
    machine_name="your-machine-name",
)
execution = executor.run(circuit, shots=1000)
print(execution.results)
```
