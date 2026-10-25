"""Shared value types.

Added during the modernisation push (era 2) and adopted unevenly: the API layer
and the newer billing helpers use these, but a lot of era-1 code still passes
raw sqlite rows and tuples around. Money is always integer cents.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Contract:
    rate_pct: int
    payer_id: str | None = None
    effective_date: str | None = None
    end_date: str | None = None


@dataclass
class StatementLine:
    claim_id: str
    service_date: str
    charge_cents: int
    is_voided: bool = False


@dataclass
class Statement:
    patient_id: str
    total_charges_cents: int
    total_adjustments_cents: int
    balance_cents: int
    lines: list[StatementLine] = field(default_factory=list)
    statement_id: str | None = None
