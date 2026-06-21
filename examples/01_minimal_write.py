# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Minimal example: parse a camt.053 XML string and write it to Excel.

Run with ``python examples/01_minimal_write.py``. The output file
``out_minimal.xlsx`` is written to the current directory.
"""

from pathlib import Path

from camt053 import parse_document

from camt053_writer_xlsx import write_xlsx

XML = """<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.08">
  <BkToCstmrStmt>
    <GrpHdr>
      <MsgId>MSG-DEMO-1</MsgId>
      <CreDtTm>2026-06-21T10:00:00</CreDtTm>
    </GrpHdr>
    <Stmt>
      <Id>STMT-1</Id>
      <ElctrncSeqNb>1</ElctrncSeqNb>
      <CreDtTm>2026-06-21T10:00:00</CreDtTm>
      <Acct><Id><IBAN>DE89370400440532013000</IBAN></Id></Acct>
      <Bal>
        <Tp><CdOrPrtry><Cd>OPBD</Cd></CdOrPrtry></Tp>
        <Amt Ccy="EUR">1000.00</Amt>
        <CdtDbtInd>CRDT</CdtDbtInd>
        <Dt><Dt>2026-06-20</Dt></Dt>
      </Bal>
    </Stmt>
  </BkToCstmrStmt>
</Document>"""


def main() -> None:
    """Parse the demo XML and write the workbook."""
    document = parse_document(XML)
    out = Path("out_minimal.xlsx")
    write_xlsx(document, out)
    print(f"Wrote {out.resolve()}")


if __name__ == "__main__":
    main()
