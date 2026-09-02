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

# Release notes

Release notes record user-visible changes for each published version.

## Versions

- [0.1.0b1](0.1.0b1.md) — Initial beta release

## Adding a release

Each release follows this structure:

1. `releasenotes/<version>.md` uses the exact PEP 440 version from
   `pyproject.toml`.
2. The version list is ordered newest first.
3. User-visible changes are grouped under `Added`, `Changed`, `Fixed`, and
   `Removed`, with empty sections omitted.
4. The package version, `cqlib_pulse.__version__`, and release-note filename
   match.
