# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""Excel (.xlsx) writer for camt053-parsed bank statements.

Exposes :func:`write_xlsx`, which serialises a
:class:`camt053.models.ParsedDocument` (the return shape of
:func:`camt053.parse.statement_parser.parse_document`) to a multi-sheet
``.xlsx`` workbook suitable for accountants and auditors.
"""

from camt053_writer_xlsx.writer import write_xlsx

__version__ = "0.0.23"

__all__ = ["write_xlsx", "__version__"]
