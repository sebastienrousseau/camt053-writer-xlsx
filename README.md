# camt053-writer-xlsx: Excel writer for parsed camt.053 statements

<p align="center">
  <img src="https://cloudcdn.pro/camt053/v1/logos/camt053.svg" alt="camt053-writer-xlsx logo" width="128" />
</p>

[![PyPI Version][pypi-badge]][07]
[![Python Versions][python-versions-badge]][07]
[![License][license-badge]][01]
[![Tests][tests-badge]][tests-url]
[![Quality][quality-badge]][quality-url]

**An Excel `.xlsx` writer for [`camt053`][core]-parsed ISO 20022 bank
statements** — turn a `ParsedDocument` into a four-sheet workbook
(Metadata, Balances, Entries, Reversals) that accountants, auditors,
and reconciliation macros can consume directly.

> **Latest release: v0.0.1** — single `write_xlsx(document, path)`
> function, 100% line + branch coverage, 100% docstring coverage.

## Contents

- [Overview](#overview)
- [Install](#install)
- [Quick Start](#quick-start)
- [Sheets](#sheets)
- [Examples](#examples)
- [The camt053 suite](#the-camt053-suite)
- [When not to use camt053-writer-xlsx](#when-not-to-use-camt053-writer-xlsx)
- [Development](#development)
- [Security](#security)
- [Documentation](#documentation)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Overview

`camt053-writer-xlsx` is a small, focused companion to the [`camt053`][core]
ISO 20022 cash-management library. It does one thing well: given a parsed
camt.053 document, write a multi-sheet Excel workbook in a stable column
layout so downstream tooling can target columns by name without parsing
the document model.

This package is part of the **camt053 suite** — a set of independently
installable packages that share the `camt053.services` layer:

- [`camt053`][core] — the core library (CLI + REST API)
- [`camt053-mcp`][mcp] — the **Model Context Protocol** server for AI agents
- [`camt053-lsp`][lsp] — the **Language Server Protocol** server for editors
- `camt053-writer-xlsx` — this package, the Excel writer

## Install

`camt053-writer-xlsx` runs on macOS, Linux, and Windows and requires
**Python 3.10+** and **pip**. It pulls in `camt053` and `openpyxl`
automatically.

```bash
pip install camt053-writer-xlsx
```

## Quick Start

```python
from camt053 import parse_document
from camt053_writer_xlsx import write_xlsx

with open("statement.xml") as fh:
    document = parse_document(fh.read())

write_xlsx(document, "statement.xlsx")
```

That's a four-sheet Excel workbook ready for your accountant.

## Sheets

| Sheet | Granularity | Use |
| :--- | :--- | :--- |
| Metadata | One row per statement | Header fields, account identifiers, balance / entry counts |
| Balances | One row per balance | Type code, amount, currency, credit/debit indicator, date |
| Entries | One row per `(entry, detail)` pair | Flattened so pivot tables and accounting macros work directly |
| Reversals | Filter of Entries | Entries with `reversal_indicator=True` or any return reason code |

The column layout is **stable across releases**; downstream tooling can
target columns by name without parsing the document model. Multi-detail
entries are flattened (an entry with N transaction details produces N
rows that share the entry-level columns), so the workbook stays
rectangular for spreadsheet consumers.

## Examples

Two runnable examples live in `examples/`:

- [`01_minimal_write.py`](examples/01_minimal_write.py) — parse a
  camt.053 XML string and write it to Excel.
- [`02_filter_reversals.py`](examples/02_filter_reversals.py) — build
  a `ParsedDocument` programmatically and inspect the Reversals sheet.

Both are exercised in CI on every commit.

## The camt053 suite

`camt053-writer-xlsx` is part of a set of independently installable
packages built around the [`camt053`][core] library — pick whichever
ones your stack needs:

| Package | Role |
| :--- | :--- |
| [`camt053`](https://pypi.org/project/camt053/) | Core library + CLI + FastAPI REST API |
| [`camt053-mcp`](https://pypi.org/project/camt053-mcp/) | Model Context Protocol server (for AI agents) |
| [`camt053-lsp`](https://pypi.org/project/camt053-lsp/) | Language Server Protocol server (for editors) |
| [`camt053-writer-xlsx`](https://pypi.org/project/camt053-writer-xlsx/) | **Excel `.xlsx` writer (this package)** |
| [`camt053-loader-mt940`](https://pypi.org/project/camt053-loader-mt940/) | SWIFT MT940 → camt.053 loader |

```mermaid
flowchart LR
    A["camt.053 XML"] -->|parse_document| B["camt053"]
    B -->|ParsedDocument| C["camt053-writer-xlsx"]
    C -->|.xlsx workbook| D["Accountants / auditors"]
```

## When not to use camt053-writer-xlsx

- **You need a custom sheet layout.** The four-sheet structure
  (Metadata / Balances / Entries / Reversals) is stable by design
  so downstream tooling can target columns by name. Forking the
  writer is the right move if your downstream needs differ.
- **You need `.xls` (legacy binary).** `openpyxl` writes `.xlsx`
  only; convert downstream if you must.
- **You need encrypted output.** Out of scope; encrypt the produced
  `.xlsx` downstream with a tool like `msoffcrypto-tool`.
- **You want to *read* Excel.** This package is a writer. The
  inverse direction (`.xlsx` → camt.053) is not currently in the
  suite; open an issue if you'd find it useful.

## Development

```bash
git clone https://github.com/sebastienrousseau/camt053-writer-xlsx
cd camt053-writer-xlsx
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                       # 100% line + branch coverage gate
interrogate camt053_writer_xlsx  # 100% docstring gate
mypy camt053_writer_xlsx     # strict
```

## Security

`camt053-writer-xlsx` consumes already-parsed data, not raw XML — the
XXE / billion-laughs surface lives upstream in the `camt053` core.
Reporting practice, supported versions, and supply-chain posture
(PyPI Trusted Publishing, sigstore attestations, signed tags) are
documented in [`SECURITY.md`](SECURITY.md). Vulnerabilities go via
GitHub Private Vulnerability Reporting, not public issues.

## Documentation

- [`README.md`](README.md) — this file
- [`CHANGELOG.md`](CHANGELOG.md) — release notes
- [`SECURITY.md`](SECURITY.md) — disclosure + supported versions
- [`SUPPORT.md`](SUPPORT.md) — how to get help
- [`MAINTAINERS.md`](MAINTAINERS.md) — who can merge
- [`examples/`](examples/) — runnable scripts, exercised in CI

## License

Licensed under the [Apache License, Version 2.0][01]. Any contribution
submitted for inclusion shall be licensed as above, without additional
terms.

## Contributing

Contributions are welcome — open an issue or PR on
[the repository](https://github.com/sebastienrousseau/camt053-writer-xlsx).

## Acknowledgements

Built on the [`camt053`][core] ISO 20022 Bank Statement library and
[openpyxl](https://openpyxl.readthedocs.io/).

[01]: https://opensource.org/license/apache-2-0/
[07]: https://pypi.org/project/camt053-writer-xlsx/
[core]: https://github.com/sebastienrousseau/camt053
[mcp]: https://github.com/sebastienrousseau/camt053-mcp
[lsp]: https://github.com/sebastienrousseau/camt053-lsp
[pypi-badge]: https://img.shields.io/pypi/v/camt053-writer-xlsx.svg?style=for-the-badge
[python-versions-badge]: https://img.shields.io/pypi/pyversions/camt053-writer-xlsx.svg?style=for-the-badge
[license-badge]: https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge
[tests-badge]: https://img.shields.io/github/actions/workflow/status/sebastienrousseau/camt053-writer-xlsx/ci.yml?branch=main&label=Tests&style=for-the-badge
[tests-url]: https://github.com/sebastienrousseau/camt053-writer-xlsx/actions/workflows/ci.yml
[quality-badge]: https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge
[quality-url]: https://github.com/sebastienrousseau/camt053-writer-xlsx/actions/workflows/ci.yml
