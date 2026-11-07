"""Stage 8 regression tests for the two prepared defects F8-01 and F8-02.

Each test uses its own fresh store and synthetic data, so the tests do not
depend on each other. They are retained after the repairs so the defects
cannot silently come back.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def test_f8_01_same_practitioner_same_time_is_rejected() -> None:
    """F8-01: FR-05, BR-05, AC-04.1 and AC-04.2.

    A second SCHEDULED booking for the same practitioner at exactly the
    same datetime is rejected and leaves the store unchanged. A different
    practitioner at that same datetime is still allowed.
    """
    # One shared store for this test, with the three services using it.
    data_store = SmartCareDataStore()
    patient_service = PatientService(data_store)
    practitioner_service = PractitionerService(data_store)
    appointment_service = AppointmentService(data_store)

    # Synthetic participants: two patients and two practitioners.
    patient_service.register_patient('P1', 'Alex Example')
    patient_service.register_patient('P2', 'Sam Example')
    practitioner_service.register_practitioner('D1', 'Taylor Example', 'General')
    practitioner_service.register_practitioner('D2', 'Morgan Example', 'General')

    when = datetime(2026, 10, 1, 9)

    # First booking for D1 at 09:00 is valid. Keep the returned object.
    first = appointment_service.book_appointment('A1', 'P1', 'D1', when)

    # Same practitioner (D1) at the exact same time must be rejected (AC-04.1).
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P2', 'D1', when)

    # Rejection must not change state: only A1 is stored, and A2 was not created.
    assert data_store.list_appointments() == [first]
    assert data_store.find_appointment('A2') is None

    # A different practitioner (D2) at the same time is allowed (AC-04.2).
    other = appointment_service.book_appointment('A3', 'P2', 'D2', when)
    assert other.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first, other]


def test_f8_02_cancelled_appointment_stays_findable() -> None:
    """F8-02: FR-06, FR-07, FR-08, BR-07, AC-05.2 and AC-05.3.

    A cancelled appointment stays stored and can still be found by the
    store and the service as the same object. Cancelling it again is
    rejected without changing its status.
    """
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General',
    )
    appointment_service = AppointmentService(data_store)

    # Book A1 and keep the exact object that was stored.
    booked = appointment_service.book_appointment(
        'A1', 'P1', 'D1', datetime(2026, 10, 1, 9),
    )

    # Cancelling returns the same object, now CANCELLED.
    cancelled = appointment_service.cancel_appointment('A1')
    assert cancelled is booked
    assert cancelled.status is AppointmentStatus.CANCELLED

    # Retained history (AC-05.2). The store lookup must return the same
    # object, not None. Checked separately from the service so that None
    # (store) and LookupError (service) are not confused.
    assert data_store.find_appointment('A1') is booked
    assert appointment_service.find_appointment('A1') is booked
    assert data_store.list_appointments() == [booked]

    # Repeated cancellation is rejected (AC-05.3) and does not change state.
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert booked.status is AppointmentStatus.CANCELLED