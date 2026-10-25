# billing/render_legacy.py  --  DEPRECATED (ADR-004). Frozen for deletion.
# One caller remains (the legacy statement.txt endpoint). Do not extend or add
# callers; do not delete while that caller exists.

def render_statement_legacy(statement):
    # produces the old fixed-width text statement. one downstream consumer still
    # parses this exact format, so the column widths are load-bearing.
    lines = []
    lines.append("STATEMENT (legacy format)")
    lines.append("PATIENT: %s" % statement.patient_id)
    lines.append("-" * 32)
    for ln in statement.lines:
        # amounts printed in cents; the header lies and says USD, ignore it
        flag = "VOID" if ln.is_voided else "    "
        lines.append("%-12s %10d %s" % (ln.claim_id, ln.charge_cents, flag))
    lines.append("-" * 32)
    lines.append("CHARGES   %10d" % statement.total_charges_cents)
    lines.append("ADJUST    %10d" % statement.total_adjustments_cents)
    lines.append("BALANCE   %10d" % statement.balance_cents)
    return "\n".join(lines)
