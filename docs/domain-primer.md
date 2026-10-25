# Domain primer: claims, contracts, statements

One page, plain language, for engineers new to healthcare billing. Enough to
work safely in this repo; not a substitute for a real revenue-cycle course.

## The objects

- **Patient**: a person we bill. Has a **payer** (their insurer) and, for our
  purposes, a name and an **MRN** (medical record number). Name and MRN are
  sensitive: they must never appear in logs.
- **Claim**: a request for payment for one episode of care. Has a **charge**
  (what we billed, in cents), an optional **adjustment** (a write-down we
  applied: a discount, a correction), a **service date** (when care happened),
  and a status. A claim can be **voided** (cancelled).
- **Payer**: the insurer. Each payer has one or more **contracts**.
- **Contract**: the agreement in force for a payer over a date range, whose
  key term here is the **allowed rate**: the percentage of the charge the payer
  is expected to cover. Contracts **renew**, so the rate that applies depends on
  the claim's service date.
- **Remittance**: money actually received from a payer against a claim.
- **Statement**: what we send the patient: their claims, the adjustments, and
  the **balance** they owe.

## How a balance is worked out

For a patient's statement:

```
total charges      = sum of claim charges
total adjustments  = sum of claim adjustments
balance            = total charges − total adjustments − payments received
```

The **contract allowed rate** is used to estimate what a payer will cover on
claims not yet paid; it is reported on the statement but is a separate figure
from the balance above.

## The rule that trips people up

A claim's correct allowed rate depends on the **service date**, not on today.
When a contract has renewed, a claim for care given *before* the renewal must
still use the *old* rate. Using "the current contract" for an older claim bills
it wrong. This matters most at year boundaries, e.g., a December visit billed in
January.

## Voiding

A voided claim must disappear from the patient's statement and statement
history. How a claim gets voided has changed over the years; the details are in
the code and in `docs/adr/ADR-002`.
