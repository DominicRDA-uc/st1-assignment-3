"""Stage 9 integrated service workflow test using synthetic data."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


T9 = datetime(2026, 11, 8, 9, 0)


def test_integrated_service_workflow() -> None:

    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)

    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'John Example', 'Skin')

    first_appointment = appointments.book_appointment('A1', 'P1', 'D1', T9)

    before_state = data_store.list_appointments()
    
    with pytest.raises(ValueError):
        appointments.book_appointment('A1', 'P1', 'D2', T9)
    with pytest.raises(ValueError):
        appointments.book_appointment('A3', 'P1', 'D1', T9)
    with pytest.raises(LookupError):
        appointments.book_appointment('A4', 'P9', 'D1', T9)
    with pytest.raises(LookupError):
        appointments.book_appointment('A4', 'P1', 'D9', T9)
    
    assert data_store.list_appointments() == before_state
    
    with pytest.raises(LookupError):
        appointments.find_appointment('A3')
    with pytest.raises(LookupError):
        appointments.find_appointment('A4')

    second_appointment = appointments.book_appointment('A2', 'P1', 'D2', T9)
    
    assert appointments.list_practitioner_appointments('D2') == [second_appointment]
    assert appointments.list_practitioner_appointments('D1') == [first_appointment]

    appointments.cancel_appointment('A1')
    
    assert appointments.find_appointment('A1') is first_appointment 
    assert first_appointment.status is AppointmentStatus.CANCELLED
    assert appointments.list_practitioner_appointments('D1') == [first_appointment]
    assert appointments.list_practitioner_appointments('D1', AppointmentStatus.SCHEDULED) == []

    third_appointment = appointments.book_appointment('A3', 'P1', 'D1', T9)
    assert appointments.list_practitioner_appointments('D1') == [first_appointment, third_appointment]
    assert appointments.list_practitioner_appointments('D1', AppointmentStatus.SCHEDULED) == [third_appointment]
    assert appointments.list_practitioner_appointments('D1', AppointmentStatus.CANCELLED) == [first_appointment]
    assert appointments.list_practitioner_appointments('D1', AppointmentStatus.COMPLETED) == []
    
    assert data_store.list_appointments() == [first_appointment, second_appointment, third_appointment]
