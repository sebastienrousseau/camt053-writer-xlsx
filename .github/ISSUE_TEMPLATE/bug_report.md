---
name: Bug report
about: Report a defect so we can reproduce and fix it
title: "bug: "
labels: ["bug"]
assignees: []
---
<!-- SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com> -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

## Summary

A clear and concise description of the bug.

## Steps to Reproduce

1. ...
2. ...
3. ...

```python
# Minimal, self-contained snippet that triggers the bug: the
# ParsedDocument (built in code, or the camt.053 XML it was parsed from,
# redacted of account numbers and names) and the write_xlsx call.
```

## Expected Behaviour

What you expected the workbook to contain: the sheet, the row and the
column.

## Actual Behaviour

What it contains instead, or the full traceback.

## Environment

- camt053-writer-xlsx version:
- camt053 version:
- openpyxl version:
- Python version:
- Operating system:
- Spreadsheet application and version, if the problem shows there:

## Additional Context

Add any other context here: the bank that produced the statement, or the
macro or pivot table that reads the workbook.
