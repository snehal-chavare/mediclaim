"""Patient contact lookups with a small in-process cache (2022).

Goes through the repository layer (the modernisation team migrated notify onto
it). Known wart: the cache has no expiry. If a patient's contact details change
after the process started, the cache keeps serving the old value until restart.
Left as-is; low volume. (A capstone-fallback task adds invalidation.)
"""
from __future__ import annotations

from typing import Optional

from medclaim.repo import PatientRepository

_CONTACT_CACHE: dict[str, Optional[str]] = {}
_patients = PatientRepository()


def get_contact_email(patient_id: str) -> Optional[str]:
    if patient_id in _CONTACT_CACHE:
        return _CONTACT_CACHE[patient_id]
    row = _patients.get(patient_id)
    email = row["contact_email"] if row else None
    _CONTACT_CACHE[patient_id] = email
    return email


def clear_cache() -> None:
    _CONTACT_CACHE.clear()
