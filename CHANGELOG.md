# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
This package's version follows the [`camt053`](https://github.com/sebastienrousseau/camt053)
suite (`camt053`, `camt053-mcp`, `camt053-lsp`); a `0.0.X` release of
this package targets the `0.0.X` release of `camt053`.

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
