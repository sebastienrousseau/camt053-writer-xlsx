#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""What writing a statement to a workbook costs, in time and in memory.

Time is the less interesting half. Writing xlsx means building the entire
workbook in memory before anything reaches disk, so the number that
actually decides whether a job survives is **peak memory**.

A treasury team exporting a month across a few dozen accounts is asking
for tens of thousands of rows. The output file stays small -- xlsx is
zipped XML and compresses extremely well -- so file size is a bad proxy
for what the process needs. On current `main` the peak is roughly sixty
to seventy times the size of the file finally written: a 0.4 MB workbook
costs around 28 MB of peak heap. An export that works fine on a laptop
can be killed in a container sized from the output.

That multiple is the headline number here, and it is why this measures
memory at all rather than only timing the call.

Three things are measured:

* **Time per row**, across row counts. Roughly flat means linear.
* **Peak memory**, and the ratio of peak to the size of the file
  written. That multiple says how much headroom a process needs relative
  to the output it produces.
* **Growth exponent** for both time and peak, so a change that turns
  either superlinear shows up as a number rather than as a shape
  somebody has to eyeball.

One honest limit: peak memory comes from :mod:`tracemalloc`, which sees
Python-level allocations only. Whatever the zip encoder allocates in C is
not counted, so the real peak is somewhat higher than the figure printed.
Treat it as a floor and a way to compare runs, not as a budget.

Run::

    python benches/bench_write_xlsx.py
    python benches/bench_write_xlsx.py --json
    python benches/bench_write_xlsx.py --quick     # what CI runs

Nothing here asserts a threshold: wall-clock and memory are not
comparable between machines, and a flaky performance gate teaches people
to ignore red. CI runs ``--quick`` so a benchmark that has stopped
compiling against the current API fails the build instead of rotting into
a file that reads as verified and is not.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
import time
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from camt053.models import (  # noqa: E402
    Account,
    Balance,
    Entry,
    ParsedDocument,
    Statement,
    TransactionDetails,
)

from camt053_writer_xlsx import write_xlsx  # noqa: E402


def _entry(index: int) -> Entry:
    """One statement entry, with details, distinct per index."""
    return Entry(
        amount=f"{(index % 900) + 100}.00",
        currency="EUR",
        credit_debit_indicator="CRDT" if index % 2 else "DBIT",
        status="BOOK",
        booking_date="2026-06-21",
        value_date="2026-06-21",
        account_servicer_ref=f"ASR-{index}",
        reversal_indicator=index % 25 == 0,
        reason_code="AC04" if index % 25 == 0 else None,
        details=[
            TransactionDetails(
                end_to_end_id=f"E2E-{index}",
                tx_id=f"TX-{index}",
                instruction_id=f"INSTR-{index}",
                reason_code=None,
                counterparty_name=f"Counterparty {index}",
                counterparty_account="FR1420041010050500013M02606",
                additional_info=f"Invoice {index}",
            )
        ],
    )


def build(entries: int) -> ParsedDocument:
    """A single-statement document carrying ``entries`` entries."""
    return ParsedDocument(
        message_type="camt.053.001.08",
        msg_id=f"MSG-BENCH-{entries}",
        creation_date_time="2026-06-21T10:00:00",
        statements=[
            Statement(
                id=f"STMT-BENCH-{entries}",
                electronic_seq_nb="1",
                creation_date_time="2026-06-21T10:00:00",
                account=Account(
                    iban="DE89370400440532013000",
                    other_id=None,
                    currency="EUR",
                    owner_name="ACME GmbH",
                    servicer_bic="COBADEFFXXX",
                ),
                balances=[
                    Balance(
                        type_code="OPBD",
                        amount="1000.00",
                        currency="EUR",
                        credit_debit_indicator="CRDT",
                        date="2026-06-20",
                    ),
                    Balance(
                        type_code="CLBD",
                        amount="1500.00",
                        currency="EUR",
                        credit_debit_indicator="CRDT",
                        date="2026-06-21",
                    ),
                ],
                entries=[_entry(i) for i in range(entries)],
            )
        ],
    )


def _exponent(points: list[tuple[int, float]]) -> float | None:
    """Log-log slope across the measured range: 1.0 linear, 2.0 quadratic."""
    if len(points) < 2:
        return None
    (n0, v0), (n1, v1) = points[0], points[-1]
    if n0 == n1 or v0 <= 0 or v1 <= 0:
        return None
    return math.log(v1 / v0) / math.log(n1 / n0)


def measure(entries: int, repeats: int) -> dict:
    """Time, peak memory and output size for an ``entries``-row export."""
    document = build(entries)
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "bench.xlsx"

        # Timed separately from the memory run: tracemalloc adds real
        # overhead to every allocation, so timing under it would measure
        # the profiler as much as the writer.
        write_xlsx(document, target)
        samples = []
        for _ in range(repeats):
            start = time.perf_counter()
            write_xlsx(document, target)
            samples.append(time.perf_counter() - start)
        seconds = min(samples)

        tracemalloc.start()
        write_xlsx(document, target)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        written = target.stat().st_size

    return {
        "entries": entries,
        "ms": seconds * 1e3,
        "us_per_row": seconds * 1e6 / entries,
        "peak_mb": peak / 1e6,
        "file_mb": written / 1e6,
        "peak_over_file": peak / written if written else 0.0,
    }


def run(quick: bool) -> dict:
    sizes = [100, 500] if quick else [100, 1_000, 5_000]
    repeats = 1 if quick else 3
    rows = [measure(n, repeats) for n in sizes]
    return {
        "rows": rows,
        "time_exponent": _exponent([(r["entries"], r["ms"]) for r in rows]),
        "peak_exponent": _exponent(
            [(r["entries"], r["peak_mb"]) for r in rows]
        ),
    }


def _shape(exponent: float | None) -> str:
    """Describe a growth exponent without flattering it.

    Below 1.0 does not mean sublinear work: it means the fixed
    per-workbook cost (metadata sheets, styles, the zip container) is
    still being spread over too few rows to have amortised. Calling that
    "linear" would be reading a small-sample artefact as a result.
    """
    if exponent is None:
        return "not enough sizes to say"
    if exponent < 0.8:
        return "fixed per-workbook cost still dominating at these sizes"
    if exponent <= 1.25:
        return "linear, as it should be"
    if exponent < 1.75:
        return "superlinear -- worth a look"
    return "quadratic -- something is rebuilding per row"


def render(results: dict) -> None:
    print(
        f"  {'entries':>9}{'ms':>10}{'us/row':>10}{'peak MB':>11}"
        f"{'file MB':>10}{'peak/file':>12}"
    )
    for row in results["rows"]:
        print(
            f"  {row['entries']:>9}{row['ms']:>10.1f}{row['us_per_row']:>10.1f}"
            f"{row['peak_mb']:>11.2f}{row['file_mb']:>10.3f}"
            f"{row['peak_over_file']:>11.1f}x"
        )
    time_exp = results["time_exponent"]
    peak_exp = results["peak_exponent"]
    print(
        f"\n  time growth exponent {time_exp:.2f} -- {_shape(time_exp)}."
        if time_exp is not None
        else "\n  time growth: not enough sizes."
    )
    print(
        f"  peak growth exponent {peak_exp:.2f} -- {_shape(peak_exp)}."
        if peak_exp is not None
        else "  peak growth: not enough sizes."
    )
    worst = max(r["peak_over_file"] for r in results["rows"])
    print(
        f"\n  Peak heap runs about {worst:.0f}x the size of the file "
        f"written. xlsx is zipped XML and\n  compresses hard, so output "
        f"size is a bad proxy for what the process needs: an export\n  "
        f"sized from the file will be killed in a container long before "
        f"the disk notices."
    )
    print(
        "\n  Peak comes from tracemalloc, which sees Python allocations "
        "only -- whatever the zip\n  encoder allocates in C is not "
        "counted. Read it as a floor and a way to compare runs."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--quick", action="store_true", help="small sizes, as CI runs"
    )
    args = parser.parse_args()

    results = run(quick=args.quick)
    if args.json:
        json.dump(results, sys.stdout, indent=1)
        print()
    else:
        render(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
