"""Data-access layer (2022, modernisation push).

The intent was to route all SQL through repository classes. It got about halfway:
`notify/` was migrated onto the repository layer (see patient_repo.py), but
`billing/` and most of `claims/` still hit SQLite directly. Don't assume this is
the only data path in the codebase.
"""
from __future__ import annotations

from typing import Optional

from medclaim import db


class ClaimRepository:
    def by_patient(self, patient_id: str, include_voided: bool = False) -> list:
        conn = db.connect()
        try:
            if include_voided:
                rows = conn.execute(
                    "select * from claims where patient_id = ? order by service_date",
                    (patient_id,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "select * from claims where patient_id = ? and is_deleted is not 1 "
                    "order by service_date",
                    (patient_id,),
                ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get(self, claim_id: str) -> Optional[dict]:
        conn = db.connect()
        try:
            row = conn.execute("select * from claims where id = ?", (claim_id,)).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
