"""Focused tests for appointment rescheduling."""

from datetime import datetime, timezone

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


OLD_TIME = datetime(2026, 10, 1, 9)
NEW_TIME = datetime(2026, 10, 1, 11)


def rescheduling_context() -> tuple[
    SmartCareDataStore,
    AppointmentService,
    Appointment,
]:
    """Create one registered, scheduled appointment and its store."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    appointment_service = AppointmentService(data_store)
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        OLD_TIME,
    )
    return data_store, appointment_service, appointment


def appointment_snapshot(
    data_store: SmartCareDataStore,
    appointment: Appointment,
) -> tuple[object, ...]:
    """Capture appointment fields and stored collection for failure checks."""
    return (
        appointment.appointment_id,
        appointment.patient,
        appointment.practitioner,
        appointment.date_time,
        appointment.status,
        data_store.list_appointments(),
    )


def test_valid_move_preserves_appointment_and_participant_identities() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    patient = appointment.patient
    practitioner = appointment.practitioner

    moved = appointment_service.reschedule_appointment('A1', NEW_TIME)

    assert moved is appointment
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == NEW_TIME
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [appointment]


def test_service_returns_same_stored_object_after_move() -> None:
    _, appointment_service, appointment = rescheduling_context()

    assert appointment_service.reschedule_appointment('A1', NEW_TIME) is appointment


def test_domain_reschedule_changes_time_on_the_same_object() -> None:
    _, _, appointment = rescheduling_context()

    assert appointment.reschedule(NEW_TIME) is None
    assert appointment.date_time == NEW_TIME
    assert appointment.appointment_id == 'A1'


def test_valid_unknown_appointment_id_raises_lookup_error() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    before = appointment_snapshot(data_store, appointment)

    with pytest.raises(LookupError):
        appointment_service.reschedule_appointment('A9', NEW_TIME)

    assert appointment_snapshot(data_store, appointment) == before


def test_blank_appointment_id_raises_value_error() -> None:
    _, appointment_service, _ = rescheduling_context()

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment('  ', NEW_TIME)


def test_non_string_appointment_id_raises_value_error() -> None:
    _, appointment_service, _ = rescheduling_context()

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment(1, NEW_TIME)


def test_non_datetime_time_raises_value_error_without_mutation() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    before = appointment_snapshot(data_store, appointment)

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment('A1', '2026-10-01 11:00')

    assert appointment_snapshot(data_store, appointment) == before


def test_timezone_aware_time_raises_value_error_without_mutation() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    before = appointment_snapshot(data_store, appointment)
    aware_time = datetime(2026, 10, 1, 11, tzinfo=timezone.utc)

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment('A1', aware_time)

    assert appointment_snapshot(data_store, appointment) == before


def test_time_with_seconds_raises_value_error_without_mutation() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    before = appointment_snapshot(data_store, appointment)

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment(
            'A1',
            datetime(2026, 10, 1, 11, second=1),
        )

    assert appointment_snapshot(data_store, appointment) == before


def test_time_with_microseconds_raises_value_error_without_mutation() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    before = appointment_snapshot(data_store, appointment)

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment(
            'A1',
            datetime(2026, 10, 1, 11, microsecond=1),
        )

    assert appointment_snapshot(data_store, appointment) == before


def test_same_time_scheduled_reschedule_is_no_op() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    before = appointment_snapshot(data_store, appointment)

    assert appointment_service.reschedule_appointment('A1', OLD_TIME) is appointment
    assert appointment_snapshot(data_store, appointment) == before


def test_same_practitioner_scheduled_conflict_is_rejected_without_mutation() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    other = appointment_service.book_appointment('A2', 'P1', 'D1', NEW_TIME)
    before = appointment_snapshot(data_store, appointment)
    stored_before = data_store.list_appointments()

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment('A1', NEW_TIME)

    assert appointment_snapshot(data_store, appointment) == before
    assert data_store.list_appointments() == stored_before
    assert data_store.find_appointment('A2') is other


def test_conflict_check_excludes_the_appointment_being_moved() -> None:
    _, appointment_service, appointment = rescheduling_context()

    assert appointment_service.reschedule_appointment('A1', OLD_TIME) is appointment


def test_different_practitioner_at_new_time_is_allowed() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    PractitionerService(data_store).register_practitioner(
        'D2',
        'Morgan Example',
        'General',
    )
    other = appointment_service.book_appointment('A2', 'P1', 'D2', NEW_TIME)

    assert appointment_service.reschedule_appointment('A1', NEW_TIME) is appointment
    assert appointment.date_time == NEW_TIME
    assert other.date_time == NEW_TIME


def test_cancelled_appointment_at_new_time_does_not_conflict() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    cancelled = Appointment(
        'A2',
        appointment.patient,
        appointment.practitioner,
        NEW_TIME,
    )
    data_store.add_appointment(cancelled)
    cancelled.cancel()

    assert appointment_service.reschedule_appointment('A1', NEW_TIME) is appointment
    assert appointment.date_time == NEW_TIME
    assert cancelled.status is AppointmentStatus.CANCELLED


def test_cancelled_target_rejects_same_time_without_mutation() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    appointment.cancel()
    before = appointment_snapshot(data_store, appointment)

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment('A1', OLD_TIME)

    assert appointment_snapshot(data_store, appointment) == before


def test_completed_target_rejects_same_time_without_mutation() -> None:
    data_store, _, scheduled = rescheduling_context()
    completed = Appointment(
        'A2',
        scheduled.patient,
        scheduled.practitioner,
        NEW_TIME,
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)
    appointment_service = AppointmentService(data_store)
    before = appointment_snapshot(data_store, completed)

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment('A2', NEW_TIME)

    assert appointment_snapshot(data_store, completed) == before


def test_failed_conflicting_move_preserves_complete_store_snapshot() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    appointment_service.book_appointment('A2', 'P1', 'D1', NEW_TIME)
    appointment_before = appointment_snapshot(data_store, appointment)
    store_before = data_store.list_appointments()

    with pytest.raises(ValueError):
        appointment_service.reschedule_appointment('A1', NEW_TIME)

    assert appointment_snapshot(data_store, appointment) == appointment_before
    assert data_store.list_appointments() == store_before


def test_old_slot_can_be_booked_after_move() -> None:
    _, appointment_service, appointment = rescheduling_context()

    appointment_service.reschedule_appointment('A1', NEW_TIME)
    replacement = appointment_service.book_appointment(
        'A2',
        'P1',
        'D1',
        OLD_TIME,
    )

    assert replacement.date_time == OLD_TIME
    assert appointment.date_time == NEW_TIME


def test_lookup_and_practitioner_listing_show_new_time_in_order() -> None:
    data_store, appointment_service, appointment = rescheduling_context()
    middle = appointment_service.book_appointment(
        'A2',
        'P1',
        'D1',
        datetime(2026, 10, 1, 10),
    )
    last = appointment_service.book_appointment(
        'A3',
        'P1',
        'D1',
        datetime(2026, 10, 1, 12),
    )

    appointment_service.reschedule_appointment('A1', NEW_TIME)

    assert appointment_service.find_appointment('A1') is appointment
    assert appointment_service.find_appointment('A1').date_time == NEW_TIME
    listed = appointment_service.list_practitioner_appointments('D1')
    assert listed == [middle, appointment, last]
    assert [item.date_time for item in listed] == [
        datetime(2026, 10, 1, 10),
        NEW_TIME,
        datetime(2026, 10, 1, 12),
    ]
    assert data_store.list_appointments() == [appointment, middle, last]
