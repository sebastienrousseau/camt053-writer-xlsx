<!-- SPDX-License-Identifier: Apache-2.0 -->

# Getting support

Thanks for using `camt053-writer-xlsx`. Here's the fastest way to
get help, by need.

## Read first

- **[README.md](README.md)** — install, quick start, the four-sheet
  workbook layout.
- **[`examples/`](examples/)** — two runnable scripts exercised in CI.

## Questions & how-to

Open a [GitHub Discussion](https://github.com/sebastienrousseau/camt053-writer-xlsx/discussions)
with:

- Python version + OS
- `camt053-writer-xlsx` version + `camt053` version
- A minimal reproducer (CLI invocation or short Python snippet)
- The full error output

Cross-package questions (e.g. how does this writer interact with
camt053's REST API?) are also welcome on the parent's
[Discussions](https://github.com/sebastienrousseau/camt053/discussions).

## Bugs

Open an [issue](https://github.com/sebastienrousseau/camt053-writer-xlsx/issues/new)
with:

- The same triage data as above
- A reproducer that constructs the failing `ParsedDocument`
  (sensitive values redacted as needed)
- Expected vs. actual behaviour

## Feature requests

Likely categories:

- **Custom sheet layouts** — currently out of scope; the four-sheet
  layout is stable by design for downstream tooling.
- **`.xls` (legacy binary)** — out of scope; openpyxl writes `.xlsx`
  only.
- **Encrypted workbooks** — out of scope; encrypt downstream with
  `msoffcrypto-tool`.

Anything else? Open an issue.

## Security

**Do not** open public issues for vulnerabilities. Follow the
private disclosure process in [SECURITY.md](SECURITY.md).

## Support tiers

This package is open source under Apache-2.0. There is no paid
support tier.

- **Community support** (issues / discussions / PRs): best effort.
- **Commercial support**: not available today. Contact
  `support@camt053.com` so the maintainer can gauge demand.

## The camt053 suite

This package is one of four:

- [`camt053`](https://github.com/sebastienrousseau/camt053) — core
  library, CLI, REST API
- [`camt053-mcp`](https://github.com/sebastienrousseau/camt053-mcp)
  — MCP server (AI agents)
- [`camt053-lsp`](https://github.com/sebastienrousseau/camt053-lsp)
  — Language Server (editors)
- [`camt053-writer-xlsx`](https://github.com/sebastienrousseau/camt053-writer-xlsx)
  — **Excel writer (this package)**

Issues spanning multiple packages can be filed against `camt053`
(the core); the maintainer will route them.

## Supported versions

| Version | Supported? |
| :--- | :--- |
| 0.0.1 (latest) | ✅ |

Requires Python 3.10+ and `camt053 >= 0.0.5`.
