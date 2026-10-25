"""Patient data access (2022, modernisation push).

Part of the repository layer that the modernisation team started. `notify/` was
migrated onto it; `billing/` and `claims/` were never moved across and still hit
SQLite directly. That half-migrated state is the reality of this codebase.
"""
from __future__ import annotations

from typing import Optional

from medclaim import db


class PatientRepository:
    def get(self, patient_id: str) -> Optional[dict]:
        conn = db.connect()
        try:
            row = conn.execute(
                "select patient_id, name, mrn, payer_id, contact_email "
                "from patients where patient_id = ?",
                (patient_id,),
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
