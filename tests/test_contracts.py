from medclaim.billing import contracts


def test_current_bcbs_rate(client):
    # current-period (2024) BCBS claims resolve to 70%.
    c = contracts.resolve_contract("BCBS-001", "2024-06-15")
    assert c.rate_pct == 70


def test_aetna_rate(client):
    c = contracts.resolve_contract("AETNA-002", "2024-06-15")
    assert c.rate_pct == 75


def test_uhc_rate(client):
    c = contracts.resolve_contract("UHC-003", "2024-06-15")
    assert c.rate_pct == 85


def test_contract_for_date_matches_resolve_in_current_period(client):
    # inside the current period the two lookups agree, so statements are correct.
    for payer in ("BCBS-001", "AETNA-002", "UHC-003"):
        a = contracts.resolve_contract(payer, "2024-06-15").rate_pct
        b = contracts.contract_for_date(payer, "2024-06-15").rate_pct
        assert a == b
