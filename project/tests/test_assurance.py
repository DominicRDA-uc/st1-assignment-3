from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


OLD_TIME = datetime(2026, 10, 1, 9, 0)
NEW_TIME = datetime(2026, 10, 1, 11, 0)


def test_lookup_does_not_use_another_store() -> None:
    first = SmartCareDataStore()
    second = SmartCareDataStore()
    PatientService(first).register_patient('P1', 'Alex Example')

    with pytest.raises(LookupError) as error:
        PatientService(second).find_patient('P1')

    assert str(error.value) == 'Patient not found'
    assert 'P1' not in str(error.value)
    assert second.list_patients() == []
    assert first.find_patient('P1') is not None


def test_reschedule_keeps_cancelled_history_in_a_new_list() -> None:
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner(
        'D1', 'Taylor Example', 'General')
    appointments = AppointmentService(data_store)
    first = appointments.book_appointment('A1', 'P1', 'D1', OLD_TIME)
    appointments.cancel_appointment('A1')
    second = appointments.book_appointment('A2', 'P1', 'D1', OLD_TIME)
    
    moved = appointments.reschedule_appointment('A2', NEW_TIME)
    listed = appointments.list_practitioner_appointments('D1')
    stored = data_store.list_appointments()

    assert moved is second
    assert appointments.find_appointment('A1') is first
    assert first.status is AppointmentStatus.CANCELLED
    assert first.date_time == OLD_TIME
    assert second.date_time == NEW_TIME
    assert listed == [first, second]
    assert listed is not stored
    assert stored == [first, second]
