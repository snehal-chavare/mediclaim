"""Deterministic seed-data generator (dev tool).

Run once to (re)produce seed/data/*.json. Uses a fixed RNG seed so the dataset
is identical on every machine. build_seed.py loads the JSON into SQLite; this
file is not needed at runtime.

    python seed/generate.py
"""
import json
import random
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
RNG = random.Random(4242)

PAYERS = [
    {"payer_id": "BCBS-001", "name": "Blue Cross Blue Shield"},
    {"payer_id": "AETNA-002", "name": "Aetna"},
    {"payer_id": "UHC-003", "name": "UnitedHealthcare"},
]

# BCBS renews at the 2024 boundary (80% -> 70%). This is the contract-date trap.
CONTRACTS = [
    {"payer_id": "BCBS-001", "effective_date": "2023-01-01", "end_date": "2023-12-31", "rate_pct": 80},
    {"payer_id": "BCBS-001", "effective_date": "2024-01-01", "end_date": None, "rate_pct": 70},
    {"payer_id": "AETNA-002", "effective_date": "2023-01-01", "end_date": None, "rate_pct": 75},
    {"payer_id": "UHC-003", "effective_date": "2023-01-01", "end_date": None, "rate_pct": 85},
]

FIRST = ["James", "Mary", "Robert", "Linda", "Michael", "Patricia", "John", "Jennifer",
         "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph"]
LAST = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]


def money(lo, hi):
    return RNG.randint(lo, hi)


def build():
    patients, claims, remits = [], [], []

    # --- Explicit fixture patients the test suite and exercises depend on ---
    # P-1042: BCBS, current-period claims, used by history + build_statement tests
    #         and by the FM-Lite-01 facilitator trigger.
    patients.append({"patient_id": "P-1042", "name": "Margaret Hale", "mrn": "MRN-100142",
                     "payer_id": "BCBS-001", "contact_email": "m.hale@example.test"})
    claims.append({"id": "C-1042-01", "patient_id": "P-1042", "payer_id": "BCBS-001",
                   "service_date": "2024-03-04", "amount_cents": 22_000,
                   "adjustment_cents": 0, "status": "submitted", "is_deleted": None})
    claims.append({"id": "C-1042-02", "patient_id": "P-1042", "payer_id": "BCBS-001",
                   "service_date": "2024-04-11", "amount_cents": 9_500,
                   "adjustment_cents": 500, "status": "submitted", "is_deleted": None})

    # P-2001: AETNA, NO seeded claims -- test 4 injects its own.
    patients.append({"patient_id": "P-2001", "name": "Arthur Reed", "mrn": "MRN-100201",
                     "payer_id": "AETNA-002", "contact_email": "a.reed@example.test"})

    # P-1077: BCBS, a single LATE-DECEMBER-2023 claim -> the contract-boundary trap
    #         (ticket T-101). Correct rate is 80% (2023); the bug bills it at 70%.
    patients.append({"patient_id": "P-1077", "name": "Nadia Okafor", "mrn": "MRN-100177",
                     "payer_id": "BCBS-001", "contact_email": "n.okafor@example.test"})
    claims.append({"id": "C-1077-01", "patient_id": "P-1077", "payer_id": "BCBS-001",
                   "service_date": "2023-12-28", "amount_cents": 40_000,
                   "adjustment_cents": 0, "status": "submitted", "is_deleted": None})

    # --- Bulk patients ---
    payer_ids = [p["payer_id"] for p in PAYERS]
    for i in range(47):
        pid = f"P-{2100 + i}"
        payer = RNG.choice(payer_ids)
        patients.append({
            "patient_id": pid,
            "name": f"{RNG.choice(FIRST)} {RNG.choice(LAST)}",
            "mrn": f"MRN-{200100 + i}",
            "payer_id": payer,
            "contact_email": f"pat{i}@example.test",
        })
        for j in range(RNG.randint(2, 6)):
            # bulk claims all sit in the current (2024) contract period, so the
            # boundary trap never fires by accident in the normal dataset.
            month = RNG.randint(1, 9)
            cid = f"C-{2100 + i}-{j:02d}"
            amt = money(5_000, 60_000)
            adj = RNG.choice([0, 0, 0, 500, 1_200])
            claims.append({"id": cid, "patient_id": pid, "payer_id": payer,
                           "service_date": f"2024-{month:02d}-{RNG.randint(1,27):02d}",
                           "amount_cents": amt, "adjustment_cents": adj,
                           "status": "submitted", "is_deleted": None})
            # ~40 remittances across the dataset
            if RNG.random() < 0.22 and len(remits) < 40:
                remits.append({"id": f"R-{len(remits):03d}", "claim_id": cid,
                               "paid_cents": int(amt * 0.6), "posted_date": "2024-10-01"})

    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "payers.json").write_text(json.dumps(PAYERS, indent=2))
    (DATA / "contracts.json").write_text(json.dumps(CONTRACTS, indent=2))
    (DATA / "patients.json").write_text(json.dumps(patients, indent=2))
    (DATA / "claims.json").write_text(json.dumps(claims, indent=2))
    (DATA / "remittances.json").write_text(json.dumps(remits, indent=2))
    print(f"patients={len(patients)} claims={len(claims)} remittances={len(remits)}")


if __name__ == "__main__":
    build()
