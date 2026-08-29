# Benchmarks

Writing xlsx means building the **entire workbook in memory** before
anything reaches disk. Time matters, but the number that decides whether
an export job survives is peak memory.

## Running it

```sh
python benches/bench_write_xlsx.py           # full run
python benches/bench_write_xlsx.py --quick   # what CI runs
python benches/bench_write_xlsx.py --json    # machine-readable
```

CI runs `--quick`. Not a timing gate — wall-clock and memory are not
comparable between runners. It runs so a benchmark that has stopped
compiling against the current API fails the build rather than rotting
into a file that reads as verified and is not.

## The headline: peak is ~60–80× the file

| entries | ms | peak MB | file MB | peak/file |
|--------:|---:|--------:|--------:|----------:|
| 100 | 20.2 | 0.82 | 0.015 | 56× |
| 1000 | 155.2 | 5.09 | 0.079 | 65× |
| 5000 | 674.2 | 27.67 | 0.357 | 78× |

xlsx is zipped XML and compresses hard, so **the output file is a bad
proxy for what the process needs**. A 0.36 MB workbook costs around
28 MB of peak heap. An export sized from the file it produces will be
killed in a container that looks generously provisioned, long before the
disk notices.

Size the process from the row count instead.

## Growth

Both time and peak memory grow linearly with entries (exponent ~0.90
across 100→5000). Below about 0.8 the benchmark says so explicitly
rather than calling it linear: at small sizes the fixed per-workbook cost
— metadata sheet, styles, the zip container — has not yet amortised, and
reading that as sublinear work would be a small-sample artefact.

## One honest limit

Peak memory comes from `tracemalloc`, which sees **Python-level
allocations only**. Whatever the zip encoder allocates in C is not
counted, so the true peak is somewhat higher than the figure printed.
Read it as a floor and as a way to compare runs, not as a budget.
