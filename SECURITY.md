<!-- SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com> -->
<!-- SPDX-License-Identifier: Apache-2.0 OR MIT -->

# Security Policy

## Supported versions

This package follows the [`camt053`](https://github.com/sebastienrousseau/camt053)
suite cadence. Security patches are issued for the latest minor of
the latest major. While pre-`1.0`, that means **the latest released
0.0.x and the immediately prior 0.0.x** receive security fixes; older
0.0.x versions do not.

| Version | Status | Receives security fixes? |
| :--- | :--- | :--- |
| `0.0.24` (latest) | Current | ✅ Yes |
| `0.0.23` | Prior | ✅ Yes |

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
| **Formula injection** | Every data cell is written as a plain string or number. openpyxl stores a string that starts with `=` as a formula, so `write_xlsx` sets any such data cell back to a string: it shows the statement's text and is never evaluated. Releases up to and including 0.0.20 wrote it as a live formula (CWE-1236); see the repository's security advisories. |
| **Dependency CVEs** | `camt053 >= 0.0.24, < 1` and `openpyxl >= 3.1, < 4` are the only runtime dependencies. CI audits every hash-pinned requirements file with `pip-audit` on every pull request, and Dependabot watches them. |

### Cryptography status

This package implements **no** cryptographic functionality. The
underlying `openpyxl` writes the OOXML zip envelope without
performing any cryptographic signing of the workbook contents.
If you need signed-Excel output, sign the workbook downstream with
a tool like `msoffcrypto-tool`.

### Supply chain

- **PyPI Trusted Publishing** (OIDC, no long-lived tokens).
- **Sigstore attestations** for sdist + wheel via
  `pypa/gh-action-pypi-publish`, plus keyless cosign signatures and SLSA
  build provenance on the GitHub release.
- **CycloneDX SBOM** of the runtime dependency tree attached to every
  release.
- **Pinned CI**: every action is pinned by commit and every tool installs
  from a hash-pinned requirements file.
- **Signed git tags**: every release tag is signed with the
  maintainer's SSH key.
- **No `--no-verify` or `--allow-unverified` shortcuts** in any
  release workflow.

## Accepted OpenSSF Scorecard findings

The repository runs [OpenSSF Scorecard](https://scorecard.dev/) weekly and on
every push to `main`, and treats its results as advisory. The checks below
are **accepted risks**: code or configuration cannot resolve them for a
single-maintainer project, so they are recorded here to keep their status
explicit.

- **Branch-Protection**: `main` requires the `Analyze (Python) (python)`,
  `Lint & Type Check` and `Test (Python 3.11)` checks and linear history,
  enforced for admins. Scorecard's higher tiers also want required approving
  reviews, which a single maintainer cannot give to their own pull requests
  (see [`MAINTAINERS.md`](MAINTAINERS.md)).
- **Code-Review**: Scorecard expects each change to be approved by a second
  person. With one maintainer that is structurally impossible; every change
  still goes through a pull request gated by CI. Accepted until a second
  maintainer joins.
- **Maintained**: a heuristic over recent commit and issue activity that
  lags after a quiet period between suite releases.
- **CII-Best-Practices**: the project is not yet registered at
  [bestpractices.dev](https://www.bestpractices.dev/); Scorecard scores 10
  only for a Gold badge, which needs two or more significant contributors.

Every check code can satisfy is satisfied: Pinned-Dependencies (actions
pinned by commit, hash-pinned `pip` installs), Token-Permissions
(least-privilege workflow tokens), SAST (CodeQL on every push and pull
request), Fuzzing (Atheris) and Dangerous-Workflow.

## Contact

- **GitHub Private Vulnerability Reporting (preferred):**
  <https://github.com/sebastienrousseau/camt053-writer-xlsx/security/advisories/new>
- **Email:** `security@camt053.com`
