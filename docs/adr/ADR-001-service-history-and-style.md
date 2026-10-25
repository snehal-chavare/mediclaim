# ADR-001: Service history and the three coding eras

**Status:** Accepted (historical, informational)
**Date:** 2018–2026 (retrospective)

## Context

This service has been developed across roughly eight years by three teams. The
code reflects that and we have chosen **not** to rewrite it wholesale.

- **Era 1 — the original build (2018).** `billing/` and most of `claims/`.
  Procedural Python, terse names, raw SQL strings, sparse comments (some now
  misleading). `build_statement()` and the deprecated `render_statement_legacy()`
  live here.
- **Era 2 — the modernisation push (2022).** `notify/`, `repo/`, parts of
  `claims/`. Introduced dataclasses (`models.py`), type hints, and a repository
  layer (`repo/`) — but the repository layer was only half-adopted: some modules
  use it, others still hit SQLite directly.
- **Era 3 — the current team (2025+).** `api.py`, `db.py`, `models.py`. FastAPI,
  Pydantic at the boundary, docstrings, the good tests.

## Decision

New code follows era-3 conventions. Existing era-1/era-2 code is left in place
and changed only when a task requires it, with tests first. The linter is
configured to hold era-3 code to standard and to leave the older eras alone;
do not "clean up" lint in the legacy directories as a side effect of other work.

## Consequences

Naming is inconsistent across eras (`patient_id`, `pat_id`, `member_ref` all
appear). Two patterns for data access coexist. This is deliberate and is the
environment engineers actually work in.
