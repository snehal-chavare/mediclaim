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
