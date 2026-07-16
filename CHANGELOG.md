# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
This package's version follows the [`camt053`](https://github.com/sebastienrousseau/camt053)
suite (`camt053`, `camt053-mcp`, `camt053-lsp`); a `0.0.X` release of
this package targets the `0.0.X` release of `camt053`.

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
