# ADR-003: Contract resolution should use the claim service date

**Status:** Accepted — **not yet enforced everywhere**
**Date:** 2023

## Context

Payer contracts renew. The allowed rate that applies to a claim depends on the
claim's **service date**, not on the current date. `contracts.py` provides two
lookups:

- `current_contract(payer_id)` — the latest contract for a payer, ignoring date.
- `contract_for_date(payer_id, service_date)` — the contract in force on a date.

`contract_for_date` is correct for billing. `current_contract` is a convenience
that is only safe when a payer has never renewed.

## Decision

Billing code should resolve contracts with `contract_for_date`. Statements are
generated through a single wrapper, `resolve_contract(payer_id, service_date)`,
so there is one place to get this right.

## Status note

At time of writing, `resolve_contract` is **not** consistently using the service
date. This is documented here and left as-is; it surfaces as wrong allowed
amounts on statements that include claims from before a payer's most recent
renewal (most visibly, late-December care billed in January). Tracked, not fixed.
