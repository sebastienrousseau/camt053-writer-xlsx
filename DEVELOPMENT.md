<!-- SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com> -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Development

## Toolchain

Python 3.11 or newer ([toolchain policy](docs/POLICIES.md)). CI installs
every tool from hash-pinned files under `requirements/`; do the same
locally so you run what CI runs:

```sh
python -m venv .venv && . .venv/bin/activate
pip install --require-hashes -r requirements/test.txt -r requirements/lint.txt
pip install --no-deps -e .
```

`pip install -e ".[dev]"` also works and resolves the same tools without
hashes.

## Every CI gate, locally

| CI job | Local command |
| :--- | :--- |
| Test (3.11 to 3.14) | `make test` (pytest, 100% line and branch coverage; interrogate, 100% docstrings) |
| Benchmark and examples | `make benchmark examples` |
| Lint & Type Check | `make lint type-check` (ruff, ruff format, `reuse lint`, mypy strict) |
| Complexity | `make complexity` (needs `requirements/complexity.txt`) |
| Dependency audit | `make audit` (needs `requirements/audit.txt`) |
| Fuzz (Atheris) | `make fuzz` (Linux x86_64 only, needs `requirements/fuzz.txt`); `tests/test_fuzz.py` runs the same contract with Hypothesis anywhere |
| Version sources agree | `make verify-versions` |
| Release Notes Present | `releases/v<version>.md` must exist |
| DCO | every commit carries `Signed-off-by:` (`git commit -s`) |

`make check` runs all of these except the audit, which needs network
access, and Atheris, which needs Linux x86_64. CodeQL, OpenSSF Scorecard and the daily Suite Consistency check
(`python3 scripts/check_suite_consistency.py`, which queries PyPI) run only
on GitHub. The writer parses no input of its own, so both fuzzers build
arbitrary documents and check what reaches the workbook; the parsers that
build real documents are fuzzed in the core and the loaders.

## Complexity ceilings

Per function: cyclomatic 10, cognitive 15, Halstead difficulty 30, 60
lines; 500 lines per file. `complexity-baseline.json` records offenders
that predate the gate (none today) and may only shrink:
`python scripts/check_complexity.py --update` rewrites it after an
improvement, never to absorb a regression.

## Dependencies

Edit a `requirements/*.in` file, then `make pip-compile` (needs
[uv](https://docs.astral.sh/uv/)) to regenerate the `.txt` beside it.
Commit both. `requirements/runtime.in` mirrors `[project].dependencies`.

## Demo

`.github/demo.gif` is rendered from `.github/demo.tape` with `make demo`
([VHS](https://github.com/charmbracelet/vhs)), in a virtual environment
where the package is installed. Re-render it in any change that alters what
it shows.

## Tests

- `tests/test_writer.py`: the workbook, sheet by sheet and column by column.
- `tests/test_stress.py`: large and concurrent writes, marked `perf` and
  excluded by default; run with `pytest -m perf --no-cov`.
- `tests/test_fuzz.py`: Hypothesis builds arbitrary documents, any text in
  any field, and checks every one writes and reads back as the model held
  it.
- `tests/test_check_*.py`, `tests/test_verify_versions.py`: the scripts in
  `scripts/`.
- `tests/test_readme_template.py`: the README keeps the family's shape.
- `tests/test_version_sync.py`: `__version__` agrees with `pyproject.toml`.
- `tests/test_suite_conformance.py`: vendored from one canonical copy
  shared across the suite. Do not edit it here.

## Releases

The camt053 suite releases all six members at one version, core first.
A release is a `feat/v<version>` branch whose pull request carries the
version bump in `pyproject.toml`, `camt053_writer_xlsx/__init__.py`,
`CITATION.cff`, the README's latest-release callout, `SECURITY.md`, a
`CHANGELOG.md` section and `releases/v<version>.md`. After it merges, a
signed annotated tag `v<version>` with the message
`camt053-writer-xlsx v<version>` triggers `release.yml`: build, SLSA
provenance, SBOM, the GitHub release titled `camt053-writer-xlsx <version>`,
PyPI Trusted Publishing and sigstore signatures.
