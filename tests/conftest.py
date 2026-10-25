"""Pytest fixtures.

Each test runs against a fresh, seeded SQLite database in a temp dir, so tests
never touch a dev database and never see each other's writes.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from medclaim import db
from medclaim.claims import submit_claim
from seed import build_seed


class SeedHelper:
    """Small builder the tests use to add claims to the seeded database."""

    class _Claim:
        def __init__(self, claim_id):
            self.id = claim_id

    def claim(self, patient_id, amount_cents, adjustment_cents=0,
              service_date="2024-06-01", payer_id=None):
        pid_payer = payer_id or self._payer_for(patient_id)
        cid = submit_claim(patient_id, pid_payer, service_date,
                           amount_cents, adjustment_cents)
        return self._Claim(cid)

    def claims(self, patient_id, amounts_cents, adjusted=None,
               service_date="2024-06-01", payer_id=None):
        adjusted = adjusted or [0] * len(amounts_cents)
        out = []
        for amt, adj in zip(amounts_cents, adjusted):
            out.append(self.claim(patient_id, amt, adj, service_date, payer_id))
        return out

    def _payer_for(self, patient_id):
        conn = db.connect()
        try:
            row = conn.execute(
                "select payer_id from patients where patient_id = ?",
                (patient_id,),
            ).fetchone()
        finally:
            conn.close()
        return row["payer_id"] if row else "AETNA-002"


@pytest.fixture
def _seeded_db(tmp_path):
    path = str(tmp_path / "test.db")
    build_seed.build(path)
    db.set_active_db(path)
    yield path


@pytest.fixture
def client(_seeded_db):
    # the seeded database is active; tests call the module functions directly.
    return _seeded_db


@pytest.fixture
def seed(_seeded_db):
    return SeedHelper()
