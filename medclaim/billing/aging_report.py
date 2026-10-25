# billing/aging_report.py
# ORIGINAL BUILD (2019). Member-level aging report. The "member aging" product
# feature was cancelled before launch and this was never wired to anything --
# nothing imports it. Kept around because deleting things felt risky at the time.
#
# TODO(dpearce): reconcile member_ref vs patient_id before we ship this. dpearce
# left in 2021; this never shipped. Do not build on this.

from medclaim import db


def member_aging(member_ref):
    # NB: this module calls the patient key "member_ref"; the rest of the system
    # settled on patient_id. one of the reasons this never shipped.
    conn = db.connect()
    try:
        rows = conn.execute(
            "select id, service_date, amount_cents from claims "
            "where patient_id = ? and is_deleted is not 1",
            (member_ref,),
        ).fetchall()
    finally:
        conn.close()
    buckets = {"0_30": 0, "31_60": 0, "over_60": 0}
    # ... bucketing logic was never finished ...
    return buckets
