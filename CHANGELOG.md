<!-- SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com> -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
This package's version follows the [`camt053`](https://github.com/sebastienrousseau/camt053)
suite (`camt053`, `camt053-lsp`, `camt053-mcp`, `camt053-loader-mt940`,
`camt053-loader-mt942`, `camt053-writer-xlsx`), which releases every member
together at one version, core first.

## [0.0.24] - 2026-10-29

The camt053 suite's 0.0.24 release, core first. Every member drops
Python 3.10 and requires the 0.0.24 core. The workbook is unchanged.

### Removed

- **Python 3.10 is no longer supported; the floor is 3.11.** This is a
  decision for the whole camt053 suite: 3.10 reaches end of life in
  October 2026, and current Hypothesis releases need 3.11. The CI matrix
  is 3.11 to 3.14, ruff and mypy target 3.11, the `tomli` backport and
  the 3.10 `tomllib` fallback in `scripts/check_suite_consistency.py` are
  gone, and every hash-pinned `requirements/*.txt` is compiled for 3.11.
  The required `Test (Python 3.10)` check named in `SECURITY.md` becomes
  `Test (Python 3.11)`. On 3.10, pip keeps resolving 0.0.23.

### Changed

- Requires `camt053 >= 0.0.24, < 1` in `pyproject.toml` and
  `requirements/runtime.in` (which `lint.in` and `test.in` include), and
  the hash-pinned requirement files pin the published camt053 0.0.24.

## [0.0.23] - 2026-10-20

The camt053 suite's 0.0.23 release, which brings every member back to one
version after `camt053-mcp` published 0.0.22 alone. The workbook keeps the
same sheets and columns; the one change to what it holds is a control
character in statement text, which used to abort the write. The repository
is brought up to the family's supply-chain, licensing and documentation
standard.

### Security

- **Statement text that starts with `=` is written as text, not as a
  formula** (CWE-1236). openpyxl stores any string that starts with `=` as
  a formula, and `write_xlsx` passed every value to it unchanged, so a
  counterparty name, narrative or identifier beginning with `=` reached the
  workbook as a live formula, evaluated when the file was opened: for
  example `=HYPERLINK(...)` in a camt.053 `<Nm>` or an MT940 `:86:` line.
  Every data cell openpyxl marks as a formula is now set back to a string.
  Headers are fixed strings; the writer builds no formula on purpose.
  `SECURITY.md`'s threat model, which said no formula is built from
  statement input, now describes this.

### Fixed

- **A control character in statement text no longer aborts the write.**
  openpyxl refuses the C0 controls other than tab, line feed and carriage
  return with `IllegalCharacterError`, so one of them anywhere in a
  statement lost the whole workbook. camt.053 XML cannot carry them, but
  SWIFT text can: an MT940 `:86:` holding `\x0b`, parsed by
  `camt053-loader-mt940` 0.0.20, reproduced it. Each such character is now
  written as U+FFFD, so the cell shows where it was; every other value is
  written as before.
- **U+FFFE and U+FFFF no longer leave a workbook that cannot be opened.**
  Neither is an XML 1.0 character, but openpyxl writes them, and the
  worksheet is then not well-formed: `load_workbook` raised `ParseError`
  and a spreadsheet application would refuse the file. The Atheris harness
  found it. They are now written as U+FFFD, like the control characters.
- **The Suite Consistency check compares the tree with this package's own
  PyPI release.** It compared it with the core's, because the script was
  copied from the core, so it would have failed for the wrong reason as
  soon as the core released first, and could not see a version bumped here
  and never published. It is now the family's shared copy, with `THIS`
  naming this package.
- **Every restatement of the version is checked.** The README's "Latest
  release" line said v0.0.14 through the 0.0.16 and 0.0.20 releases, and
  there was no `CITATION.cff`. `scripts/verify_versions.py` now compares
  `pyproject.toml` with `__version__`, this changelog, `CITATION.cff`, the
  release notes, the README, `SECURITY.md` and the `camt053` floor, on
  every pull request and before a release is built.
- **`write_xlsx`'s docstring** promised a resolved path; it returns the path
  as given, and now says so.
- `CONTRIBUTING.md` described a loader, `SUPPORT.md` listed four suite
  members and a camt053 0.0.5 floor, and `SECURITY.md` named the same old
  floor.

### Added

- OpenSSF Scorecard, a Dependabot configuration for pip and GitHub Actions,
  a DCO check, and a `pip-audit` job over every hash-pinned requirements
  file.
- A complexity gate (`scripts/check_complexity.py` and complexipy): per
  function cyclomatic 10, cognitive 15, Halstead difficulty 30, 60 lines,
  and 500 lines per file, against a baseline that may only shrink. It is
  empty: nothing here is over a ceiling.
- `CITATION.cff`, REUSE licensing on every file (`reuse lint` in CI), a
  rendered demo, a user manual with the full column reference
  (`docs/index.md`), `docs/COMPARISON.md`, `docs/POLICIES.md`,
  `DEVELOPMENT.md`, `AGENTS.md`, a code of conduct, issue and pull request
  templates, and a `Makefile` that runs each CI gate locally.
- A CycloneDX SBOM of the runtime dependency tree on every GitHub release.
- Property-based fuzzing of `write_xlsx` (`tests/test_fuzz.py`,
  Hypothesis): arbitrary documents, any text in any field, must write and
  read back as the model held them, and the same contract as an Atheris
  harness (`fuzz/fuzz_write_xlsx.py`) in a Fuzz workflow, two minutes per
  change and thirty weekly. Both find the control-character failure above
  when run against the previous writer.

### Changed

- **Requires `camt053` 0.0.23 or newer** (was 0.0.16), still below 1. The
  suite releases core first at one version, and core 0.0.23 is the first
  to floor its advised dependencies (`fastapi` 0.109.1 for PYSEC-2024-38,
  `starlette` 1.3.1, `cryptography` 50.0.0 and others); a lower floor here
  let an older core resolve, and an affected `fastapi` with it.
  `scripts/verify_versions.py` now fails when the floor in
  `pyproject.toml` or `requirements/*.in` is not this version.
- CI and the release job install every tool from hash-pinned
  `requirements/*.txt` and pin every action by commit. The release builds
  with `--no-isolation` against the pinned backend, runs
  `twine check --strict`, and titles the GitHub release
  `camt053-writer-xlsx <version>`.
- The README follows the family template. `docs/benchmarks.md` is now
  `docs/BENCHMARKS.md`.
- The wheel declares the MIT licence classifier beside the Apache one.

## [0.0.20] - 2026-08-29

Aligns the `camt053` suite on one version number, and adds the gates this
repository was missing.

### Added

- `benches/bench_write_xlsx.py` measures time *and peak memory*. Writing
  xlsx builds the whole workbook in memory before anything reaches disk,
  and peak heap runs sixty to eighty times the size of the file finally
  written — a 0.36 MB workbook costs around 28 MB. Output size is
  therefore a bad proxy for what the process needs, and an export sized
  from the file it produces will be killed in a container that looks
  generously provisioned.
- `docs/benchmarks.md` with the measured table and the honest limit:
  `tracemalloc` sees Python allocations only, so the printed peak is a
  floor rather than a budget.
- `scripts/check_suite_consistency.py` and a scheduled `Suite
  Consistency` workflow comparing this tree, and every published member
  of the suite, against PyPI.
- `tests/test_suite_conformance.py`, the shared suite conformance gate.
- `CONTRIBUTING.md`, which the conformance gate requires.

### Changed

- Version aligned to `0.0.20` across all six `camt053` packages, which
  had drifted to `0.0.18`, `0.0.18`, `0.0.19`, `0.0.18`, `0.0.16` and
  `0.0.16`.
- `SECURITY.md`'s supported-version table, which still named `0.0.14`
  and `0.0.13` while the tree was at `0.0.16`.

## [0.0.16] - 2026-08-21

Suite release with `camt053` 0.0.16. No functional change in this
package.

### Changed

- **Version aligned to the suite.** Every package in the `camt053`
  suite ships the same number, so there is no compatibility table to
  consult. See `camt053.suite`, which a daily job checks against PyPI.

- **The `camt053` floor moves to `>=0.0.16`,** from `>=0.0.6` — a bound
  that had not been revisited in nine releases, because it still
  resolved and so never complained.

### Added

- **A version-sync test.** `pyproject.toml` and `__init__.py` state the
  version independently and nothing compared them, so a release could
  ship with the two disagreeing. It nearly did: the first attempt at
  this release landed `__init__.py` at 0.0.16 against a `pyproject.toml`
  still on 0.0.14, and every check passed.

## [0.0.14] - 2026-07-16

### Changed

- **Version** — suite-wide lockstep bump to `0.0.14`, targeting the
  `0.0.14` release of `camt053`. Dependency refresh only (the
  `camt053 >= 0.0.6, < 1` constraint already admits `0.0.14`); no
  functional changes to the writer.

## [0.0.13] - 2026-07-16

### Added

- **Load/stress test suite** (`tests/test_stress.py`) — sustained
  concurrent statement→xlsx writes, a several-thousand-entry workbook
  within wall-clock and memory-peak bounds, and a soak loop asserting
  bounded memory growth. Marked `perf` and excluded from the default
  run and its coverage gate; select with `-m perf --no-cov`.

### Changed

- **Version** — suite-wide lockstep bump to `0.0.13`. No functional
  changes to the writer.

## [0.0.9] - 2026-06-27

### Changed

- **Version** — suite-wide lockstep bump to `0.0.9`. No functional changes.

## [0.0.7] - 2026-06-22

### Added

First PyPI release of `camt053-writer-xlsx`. Exposes a single
public function, `write_xlsx`, that serialises a
`camt053.models.ParsedDocument` (the return shape of
`camt053.parse.statement_parser.parse_document`) to a multi-sheet
`.xlsx` workbook suitable for accountants and auditors.

- **Stable four-sheet layout** so downstream tooling
  (reconciliation macros, audit pivot tables) can target columns by
  name without parsing the document model:
  - `Metadata` — one row per statement (header fields, account,
    balance / entry counts).
  - `Balances` — one row per reported balance across all statements.
  - `Entries` — one row per `(entry, detail)` pair. Multi-detail
    entries are flattened so an entry with N `TransactionDetails`
    produces N rows that share the entry-level columns.
  - `Reversals` — the entries filter where `reversal_indicator` is
    true or any return reason code is present. The auditor's
    first-look view.
- **Header styling** — the first row of every sheet is bold so the
  workbook reads cleanly in Excel / Numbers / LibreOffice without
  further conditional formatting.
- **Two runnable examples** at `examples/01_minimal_write.py` and
  `examples/02_filter_reversals.py`, both exercised end-to-end in
  CI as integration tests.

### Requirements

- Python 3.10 or later.
- `camt053 >= 0.0.6, < 1` — the model types (`ParsedDocument`,
  `Statement`, `Entry`, `Balance`, `TransactionDetails`) consumed
  by `write_xlsx` are stable across the 0.0.x line.
- `openpyxl >= 3.1, < 4`.

### Quality gates

| Gate | Status |
| :--- | :--- |
| Line + branch coverage | **100%** (enforced via `--cov-fail-under=100`) |
| Docstring coverage (interrogate) | **100%** |
| ruff lint + format | clean |
| mypy `--strict` | clean |
| Examples in CI | 2/2 exercised as integration tests |

### Suite alignment

| Package | Version |
| :--- | :--- |
| [`camt053`](https://pypi.org/project/camt053/) | 0.0.6 |
| [`camt053-mcp`](https://pypi.org/project/camt053-mcp/) | 0.0.6 |
| [`camt053-lsp`](https://pypi.org/project/camt053-lsp/) | 0.0.6 |
| `camt053-writer-xlsx` (this release) | **0.0.7** |
