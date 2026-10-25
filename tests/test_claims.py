from medclaim import db
from medclaim.billing.history import get_statement_history
from medclaim.claims import submit_claim, void_claim, void_claim_legacy


def test_submit_creates_active_claim(client, seed):
    cid = submit_claim("P-1042", "BCBS-001", "2024-07-01", 12_000, 0)
    ids = [l.claim_id for l in get_statement_history("P-1042")]
    assert cid in ids


def test_modern_void_hides_claim_from_history(client):
    cid = submit_claim("P-1042", "BCBS-001", "2024-07-02", 5_000, 0)
    void_claim(cid, reason="entered in error")
    ids = [l.claim_id for l in get_statement_history("P-1042")]
    assert cid not in ids


def test_modern_void_records_in_void_log(client):
    cid = submit_claim("P-1042", "BCBS-001", "2024-07-03", 5_000, 0)
    void_claim(cid, reason="dupe")
    conn = db.connect()
    try:
        row = conn.execute(
            "select method from void_log where claim_id = ?", (cid,)
        ).fetchone()
    finally:
        conn.close()
    assert row is not None
    assert row["method"] == "modern"


def test_legacy_void_records_in_void_log(client):
    # the legacy path still records the void in the audit log.
    cid = submit_claim("P-1042", "BCBS-001", "2024-07-04", 5_000, 0)
    void_claim_legacy(cid, reason="correction")
    conn = db.connect()
    try:
        row = conn.execute(
            "select method from void_log where claim_id = ?", (cid,)
        ).fetchone()
    finally:
        conn.close()
    assert row is not None
    assert row["method"] == "legacy"
