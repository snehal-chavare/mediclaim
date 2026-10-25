"""Build a fresh SQLite database from the bundled JSON seed data.

    python seed/build_seed.py [path/to/db.sqlite]

Deterministic: same JSON in, same database out. Safe to re-run; drops and
recreates the file each time.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from medclaim import db

DATA = Path(__file__).resolve().parent / "data"


def _load(name):
    return json.loads((DATA / name).read_text())


def build(db_path: str) -> None:
    p = Path(db_path)
    if p.exists():
        p.unlink()
    db.set_active_db(str(p))
    conn = db.connect()
    db.init_schema(conn)

    conn.executemany(
        "INSERT INTO payers (payer_id, name) VALUES (:payer_id, :name)",
        _load("payers.json"))
    conn.executemany(
        "INSERT INTO contracts (payer_id, effective_date, end_date, rate_pct) "
        "VALUES (:payer_id, :effective_date, :end_date, :rate_pct)",
        _load("contracts.json"))
    conn.executemany(
        "INSERT INTO patients (patient_id, name, mrn, payer_id, contact_email) "
        "VALUES (:patient_id, :name, :mrn, :payer_id, :contact_email)",
        _load("patients.json"))
    conn.executemany(
        "INSERT INTO claims (id, patient_id, payer_id, service_date, amount_cents, "
        "adjustment_cents, status, is_deleted) VALUES (:id, :patient_id, :payer_id, "
        ":service_date, :amount_cents, :adjustment_cents, :status, :is_deleted)",
        _load("claims.json"))
    conn.executemany(
        "INSERT INTO remittances (id, claim_id, paid_cents, posted_date) "
        "VALUES (:id, :claim_id, :paid_cents, :posted_date)",
        _load("remittances.json"))
    conn.commit()
    conn.close()
    print(f"seeded {db_path}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else db.active_db_path()
    build(target)
