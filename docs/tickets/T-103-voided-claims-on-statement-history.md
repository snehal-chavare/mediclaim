# T-103 — Voided claims still appear in statement history

**Reported by:** Patient support
**Priority:** High

## What happens

A patient had a claim voided, but it still shows in their statement history.
Support confirmed the void was actioned (there's a void record), yet the claim
is still listed as if active.

## What we expect

Once a claim is voided, it should not appear in statement history.

## Notes

- Not every void reproduces this — some voided claims are correctly hidden.
- Start from the void record and work outward; the history query itself looks
  correct on inspection.

## Resolution

**Root cause:** `claims.void_claim_legacy` (ERA-import / correction flows)
recorded the void in `void_log` but never set `claims.is_deleted = 1`. The
history and statement queries hide only `is_deleted = 1` (ADR-002), so those
claims stayed listed. Voids through the modern `void_claim` were fine, which is
why only some voids reproduced.

**Fix:** `void_claim_legacy` now also sets `is_deleted = 1`. Tests cover the
legacy path in `tests/test_claims.py` and `tests/test_statement_history.py`.

**Data:** claims voided through the legacy path before the fix need the
backfill in the ADR-002 amendment.
