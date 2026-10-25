# ADR-004: Deprecate the legacy statement renderer

**Status:** Accepted
**Date:** 2024

## Context

`billing/render_legacy.py::render_statement_legacy()` is the era-1 statement
formatter. It is superseded by the rendering built into `build_statement()`,
but one caller still depends on its exact text output.

## Decision

`render_statement_legacy()` is **frozen for deletion**. Do not extend it or add
callers. Route new work through the current statement path. Removal is blocked
only by the single remaining caller; retiring that caller is out of scope for
routine work.

## Consequences

The function stays in the tree, unused-looking but not unused. An agent asked to
"clean up dead code" will be tempted to change or remove it — do not.
