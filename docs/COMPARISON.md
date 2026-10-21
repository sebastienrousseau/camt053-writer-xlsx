<!-- SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com> -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Comparison

What this compares: ways to get a camt053-parsed statement into a
spreadsheet. Checked on 2026-10-20 against `camt053-writer-xlsx` at this
commit and the `camt053` 0.0.20 CLI, from the released wheel's source.

| | camt053-writer-xlsx | `camt053 entries --export csv` 0.0.20 |
| :--- | :--- | :--- |
| Entry point | `write_xlsx(document, path)` (Python) | `camt053 entries -i statement.xml --export csv` (CLI) |
| Input | A `ParsedDocument` from any source: camt.053 XML, MT940, MT942 | A camt.053, camt.052 or camt.054 XML file, or stdin |
| Output | One `.xlsx` workbook | CSV or JSON text |
| Statement header and account | Metadata sheet | Not exported |
| Balances | Balances sheet | Not exported |
| Entries | One row per `(entry, detail)`, 18 columns including counterparty and end-to-end id | One row per entry, 8 columns: `reference`, `amount`, `currency`, `credit_debit_indicator`, `status`, `booking_date`, `value_date`, `reason_code` |
| Returned or reversed entries | Their own Reversals sheet | Filter with `--reason` |
| Filtering | None; the workbook holds the whole statement | `--reason`, `--status`, `--from`/`--to`, `--min`/`--max` |
| Extra dependency | `openpyxl` | None beyond `camt053` |
| Licence | Apache-2.0 OR MIT | Apache-2.0 OR MIT |

## When to pick which

Pick the writer when the statement goes to people who work in Excel, or to a
macro that needs the balances and the account beside the entries. Pick the
CLI export when a pipeline wants a filtered list of entries as plain text,
or when adding `openpyxl` is not an option.

## Evidence

- `camt053` 0.0.20: `camt053/cli/cli.py` (`_EXPORT_COLUMNS` lists the
  eight CSV columns; the `entries` command's `--export` accepts `csv` or
  `json`; its filters are `--reason`, `--status`, `--from`/`--to` and
  `--min`/`--max`).
- `camt053-writer-xlsx`: `camt053_writer_xlsx/writer.py` (`_METADATA_COLUMNS`,
  `_BALANCE_COLUMNS`, `_ENTRY_COLUMNS`) and `tests/test_writer.py`.
