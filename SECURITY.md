<!-- SPDX-License-Identifier: Apache-2.0 -->

# Security Policy

## Supported versions

This package follows the [`camt053`](https://github.com/sebastienrousseau/camt053)
suite cadence. Security patches are issued for the latest minor of
the latest major. While pre-`1.0`, that means **the latest released
0.0.x and the immediately prior 0.0.x** receive security fixes; older
0.0.x versions do not.

| Version | Status | Receives security fixes? |
| :--- | :--- | :--- |
| `0.0.14` (latest) | Current | ✅ Yes |
| `0.0.13` | Prior | ✅ Yes |

## Reporting a vulnerability

**Do not open a public issue for security reports.**

Use one of the following private channels:

1. **GitHub Private Vulnerability Reporting (preferred)**
   <https://github.com/sebastienrousseau/camt053-writer-xlsx/security/advisories/new>
2. **Email**: `security@camt053.com`

**Acknowledgement**: within 48 hours. **Triage**: within 7 days.
**Fix windows**: critical 7 days, high 30 days, medium 60 days, low
best-effort.

## Security posture

### Scope

This package exposes one function — `write_xlsx(document, path)` —
that serialises a `camt053.models.ParsedDocument` to a multi-sheet
`.xlsx` workbook. It does **not** parse XML, validate against
schemas, or accept untrusted input directly: every byte that reaches
the writer has already been parsed and validated by the camt053
core. The camt053 core enforces every upstream security control;
this package is a thin output adapter.

### Threat model

| Surface | How it's handled |
| :--- | :--- |
| **XML / XXE / billion-laughs** | Out of scope. Input is an already-parsed `ParsedDocument`, not raw XML. The camt053 core handles XML defence-in-depth via `defusedxml` + the `camt053.security.xml_guard` pre-flight. |
| **Path traversal** | Path is treated as a writer target. Callers must validate the path before invoking the writer. `openpyxl.save()` writes only to the supplied path. |
| **Formula injection** | All cell values are written as plain strings or numbers via `sheet.append([...])`. No formulas are constructed from user input. |
| **Dependency CVEs** | `openpyxl >= 3.1, < 4` and `camt053 >= 0.0.5, < 1` are the only direct deps. Both are pinned and audited by GitHub Dependabot. |

### Cryptography status

This package implements **no** cryptographic functionality. The
underlying `openpyxl` writes the OOXML zip envelope without
performing any cryptographic signing of the workbook contents.
If you need signed-Excel output, sign the workbook downstream with
a tool like `msoffcrypto-tool`.

### Supply chain

- **PyPI Trusted Publishing** (OIDC, no long-lived tokens).
- **Sigstore attestations** for sdist + wheel via
  `pypa/gh-action-pypi-publish`.
- **Signed git tags**: every release tag is signed with the
  maintainer's SSH key.
- **No `--no-verify` or `--allow-unverified` shortcuts** in any
  release workflow.

## Contact

- **GitHub Private Vulnerability Reporting (preferred):**
  <https://github.com/sebastienrousseau/camt053-writer-xlsx/security/advisories/new>
- **Email:** `security@camt053.com`
