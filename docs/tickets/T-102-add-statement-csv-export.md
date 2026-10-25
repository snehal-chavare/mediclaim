# T-102 — Add a CSV export of a patient statement

**Reported by:** Billing operations
**Priority:** Medium

## What we want

A way to export a single patient's current statement as CSV, for patients who
ask for their records. One row per statement line, plus a totals row.

## Acceptance

- Given a patient id, produce CSV with: claim id, service date, charge, and a
  voided flag, one row per line.
- A final row (or clearly labelled section) with total charges, total
  adjustments, and balance.
- Amounts in dollars-and-cents for the reader (the data is stored in cents).
- Covered by a test.

## Notes

A clean, bounded feature — good first ticket on this codebase.
