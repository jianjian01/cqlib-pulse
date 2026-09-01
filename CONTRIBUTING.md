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

# Contributing to cqlib-pulse

## Development setup

```bash
git clone https://github.com/ruihuang02/cqlib-pulse.git
cd cqlib-pulse
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pre-commit install
pre-commit run --all-files
python -m pytest
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Change requirements

1. Branches are based on the latest `main` branch and cover one focused change.
2. New behavior and bug fixes include corresponding tests.
3. Public behavior changes include English and Chinese documentation updates.
4. User-visible changes are recorded in the relevant `releasenotes` file.
5. New source and documentation files include the project copyright header.
6. `pre-commit run --all-files` and `python -m pytest` pass before review.

New public APIs use Python type hints and support the Python versions declared
in `pyproject.toml`.

## Pull requests

Pull request descriptions cover the problem, the chosen solution, and the
validation performed. Related issues and user-visible or compatibility changes
are included when applicable.

By submitting a contribution, you agree that it is licensed under the Apache
License 2.0 included in this repository.
