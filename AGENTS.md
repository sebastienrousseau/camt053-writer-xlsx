<!-- SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com> -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# AGENTS.md

Invariants for AI-assisted contributions to `camt053-writer-xlsx`. Read this before changing anything.

Everything here applies equally to humans and automated agents. It is addressed to agents because agents can make breaking changes across multiple files before anyone notices.

## What this repository is

`camt053-writer-xlsx` is the Excel writer of the camt053 suite: one function, `write_xlsx(document, path)`, that writes a `camt053.models.ParsedDocument` to a four-sheet workbook (Metadata, Balances, Entries, Reversals). It parses nothing itself; the core and the MT940/MT942 loaders build the document. Its core value is a workbook layout that does not move, so macros and pivot tables written against one statement work on the next.

## 1. Core Invariants

1. **Versioning**: releases stay on the `0.0.x` line and increment strictly by `0.0.1`. Version work happens on `feat/v<next-version>` only. `v0.1.0` follows `v0.0.999`.
2. **Suite lockstep**: every member ships the core's version, and the core releases first. `scripts/check_suite_consistency.py` is the shared copy every member carries (only `THIS` differs); change it in every member or not at all. The `camt053` floor in `pyproject.toml` and `requirements/runtime.in` is the newest released core.
3. **Single source of truth**: the version in `pyproject.toml` must agree with `camt053_writer_xlsx/__init__.py`, `CHANGELOG.md`, `CITATION.cff`, `releases/v<version>.md`, the README's latest-release line and `SECURITY.md` (checked by `scripts/verify_versions.py`).
4. **The layout is the contract**: renaming, reordering or removing a sheet or column, or changing what a cell holds for the same document, is breaking even when no signature moves. Add columns only at the end of a sheet, and record it in the changelog.
5. **The core decides**: parsing, validation and the model come from `camt053`. Do not reinterpret a field here; fix it in the core.
6. **Dual licensing**: Apache-2.0 OR MIT, machine-readable on every file (`reuse lint`).

## 2. Before You Claim To Be Done

```console
make check
```

It runs ruff, `reuse lint`, mypy `--strict`, the complexity gate, the version check, pytest (100% line and branch coverage), interrogate, the benchmark and the examples; CI also runs `pip-audit`, CodeQL, Scorecard and DCO. Every function stays within cyclomatic 10, cognitive 15, Halstead difficulty 30 and 60 lines, every file within 500 lines; existing offenders would be in `complexity-baseline.json` (empty today), which may only shrink.

## 3. Hygiene First

Before any feature, fix or release work: open Dependabot PRs and alerts, code-scanning and secret-scanning alerts, `pip-audit`, and a red CI on `main` are cleared first. A dependency with an advisory is floored in `pyproject.toml` (and the `requirements/*.in` it appears in) so no affected version resolves.

## 4. Leave Alone

- `tests/test_suite_conformance.py` is a vendored, checksummed copy shared across the suite; it is excluded from ruff format for that reason.
- `requirements/*.txt` are generated (`make pip-compile`); never hand-edit them.
- `.github/demo.gif` is rendered from `.github/demo.tape` by `make demo`; never edit it by hand.
