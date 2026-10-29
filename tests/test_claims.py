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


def _is_deleted(claim_id):
    conn = db.connect()
    try:
        row = conn.execute(
            "select is_deleted from claims where id = ?", (claim_id,)
        ).fetchone()
    finally:
        conn.close()
    return row["is_deleted"]


def test_legacy_void_sets_is_deleted(client):
    # T-103: the legacy path used to write void_log only, leaving the claim active.
    cid = submit_claim("P-1042", "BCBS-001", "2024-07-05", 5_000, 0)
    void_claim_legacy(cid, reason="correction")
    assert _is_deleted(cid) == 1


def test_legacy_void_hides_claim_from_history(client):
    cid = submit_claim("P-1042", "BCBS-001", "2024-07-06", 5_000, 0)
    void_claim_legacy(cid, reason="correction")
    ids = [l.claim_id for l in get_statement_history("P-1042")]
    assert cid not in ids


def test_legacy_void_hides_era1_null_claim(client):
    # C-1042-01 is an era-1 seed row (is_deleted NULL), the kind the legacy
    # ERA-import / correction flows most often void.
    assert _is_deleted("C-1042-01") is None
    void_claim_legacy("C-1042-01", reason="correction")
    assert _is_deleted("C-1042-01") == 1
    ids = [l.claim_id for l in get_statement_history("P-1042")]
    assert "C-1042-01" not in ids


def test_legacy_void_leaves_other_claims_visible(client):
    keep = submit_claim("P-1042", "BCBS-001", "2024-07-07", 5_000, 0)
    drop = submit_claim("P-1042", "BCBS-001", "2024-07-08", 5_000, 0)
    void_claim_legacy(drop, reason="correction")
    ids = [l.claim_id for l in get_statement_history("P-1042")]
    assert keep in ids
    assert "C-1042-02" in ids   # era-1 NULL row untouched
    assert drop not in ids
