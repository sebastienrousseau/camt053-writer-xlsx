<!-- SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com> -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# camt053-writer-xlsx

Write a parsed ISO 20022 **camt.053** bank statement to an Excel workbook that
an accountant, an auditor or a reconciliation macro can open directly. One
function, two arguments.

```python
from camt053_writer_xlsx import write_xlsx

write_xlsx(document, "statement.xlsx")
```

## Why this exists

Finance teams work in spreadsheets; banks send camt.053 XML. The camt053 core
reads the XML into a `ParsedDocument`, and its CLI can export the entries as
one CSV table, but a CSV of entries loses the statement around them: the
account, the opening and closing balances, and which entries were returned.

This writer keeps all of it, in a layout that does not change between
releases, so a macro or a pivot table written against one statement works on
the next one.

## The API

### `write_xlsx(document: ParsedDocument, path: str | Path) -> Path`

| | |
|---|---|
| **`document`** | A `camt053.models.ParsedDocument`: the return value of `camt053.parse_document`, or of the MT940 and MT942 loaders. |
| **`path`** | Where to write the `.xlsx` file. The parent directory must already exist; an existing file is overwritten. |
| **Returns** | `Path(path)`, the path it was given, as a `pathlib.Path`. It is not resolved to an absolute path. |
| **Raises** | `OSError` when the file cannot be written, for example a missing directory or no permission. |

The function has no options. The layout is the contract.

## The workbook

Four sheets, always in this order, each with a bold header row naming its
columns. Cells hold the values the camt053 model holds: amounts and dates are
the strings from the statement (`"1000.00"`, `"2026-06-21"`), so nothing is
rounded or reinterpreted on the way in; counts are integers and
`reversal_indicator` is a boolean. An empty field is an empty cell.

One exception: a worksheet cannot hold the C0 control characters other than
tab, line feed and carriage return. camt.053 XML cannot carry them either,
but SWIFT text can, and the MT940 loader keeps `:86:` verbatim. Each one is
written as U+FFFD, the replacement character, so the cell shows where it
was, rather than aborting the whole workbook.

A carriage return is written as it is, but XML 1.0 end-of-line handling
makes every reader of the workbook, `openpyxl` included, read `\r\n` and a
lone `\r` as `\n`.

### Metadata: one row per statement

`message_type`, `msg_id`, `creation_date_time`, `statement_id`,
`electronic_seq_nb`, `statement_creation_date_time`, `account_iban`,
`account_other_id`, `account_currency`, `account_owner_name`,
`account_servicer_bic`, `balance_count`, `entry_count`.

The first three come from the message group header and repeat on every row.

### Balances: one row per balance

`statement_id`, `type_code`, `amount`, `currency`, `credit_debit_indicator`,
`date`.

`type_code` is the ISO balance type (`OPBD`, `CLBD`, `CLAV`, ...).

### Entries: one row per entry and detail

`statement_id`, `entry_reference`, `amount`, `currency`,
`credit_debit_indicator`, `status`, `booking_date`, `value_date`,
`account_servicer_ref`, `reversal_indicator`, `entry_reason_code`,
`detail_end_to_end_id`, `detail_tx_id`, `detail_instruction_id`,
`detail_reason_code`, `detail_counterparty_name`,
`detail_counterparty_account`, `detail_additional_info`.

An entry with N transaction details produces N rows that repeat the
entry-level columns; an entry with no details produces one row whose
`detail_*` cells are empty. The sheet stays rectangular, which is what
pivot tables and lookups need. Sum `amount` over entries, not rows, when an
entry has several details.

### Reversals: the entries an auditor looks at first

The same columns as Entries, for every entry whose `reversal_indicator` is
true or that carries a return reason code, on the entry or on any of its
details (`Entry.is_returnable()`).

## Worked examples

Both run standalone with no arguments and write to the current directory:

- [`examples/01_minimal_write.py`](../examples/01_minimal_write.py): parse a
  small camt.053 XML string and write it.
- [`examples/02_filter_reversals.py`](../examples/02_filter_reversals.py):
  build a `ParsedDocument` in code, write it, and read the Reversals sheet
  back with `openpyxl`.

## Performance

Writing xlsx builds the whole workbook in memory before anything reaches
disk, and peak Python heap runs around 60 to 80 times the size of the file
finally written. Size a container from the number of rows, not from the file
it produces. [`BENCHMARKS.md`](BENCHMARKS.md) has the measured table and the
limits of the measurement.

## Related

| Package | What it does |
|---|---|
| [`camt053`](https://pypi.org/project/camt053/) | The parser and models this writer reads |
| [`camt053-loader-mt940`](https://pypi.org/project/camt053-loader-mt940/) | SWIFT MT940 to the same `ParsedDocument` |
| [`camt053-loader-mt942`](https://pypi.org/project/camt053-loader-mt942/) | SWIFT MT942 to a camt.052 `ParsedDocument` |
| [`camt053-mcp`](https://pypi.org/project/camt053-mcp/) | The same operations as agent tools |
| [`camt053-lsp`](https://pypi.org/project/camt053-lsp/) | Editor support for reversing-entry data files |

## Licence

Apache-2.0 OR MIT, at your option.
