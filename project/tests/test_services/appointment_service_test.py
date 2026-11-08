from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def book_appointment():

    data_store = SmartCareDataStore()
    appointment_service = AppointmentService(data_store)
        
    PatientService(data_store).register_patient('P1', 'Alex Example')
    PractitionerService(data_store).register_practitioner('D1','Taylor Example','General')
    
    booked = appointment_service.book_appointment('A1','P1','D1',datetime(2026, 10, 1, 9))
    
    return data_store, appointment_service, booked


def test_cancel_appointment_with_valid_id() -> None:
    
    data_store, appointment_service, booked = book_appointment()

    appointment = appointment_service.cancel_appointment('A1')

    assert appointment is booked
    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment_service.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]


def test_unknown_appointment_id() -> None:

    data_store, appointment_service, booked = book_appointment()

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A3')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment(' ')


    assert appointment_service.find_appointment('A1').status is AppointmentStatus.SCHEDULED
    assert booked.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [booked]


def test_invalid_transition_appointment() -> None:

    data_store, appointment_service, booked = book_appointment()
    completed = Appointment('A2', booked.patient, booked.practitioner, datetime(2026, 10, 1, 10), AppointmentStatus.COMPLETED)
    data_store.add_appointment(completed)

    appointment = appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A2')


    assert appointment.status is AppointmentStatus.CANCELLED
    assert completed.status is AppointmentStatus.COMPLETED
    assert data_store.list_appointments() == [appointment, completed]


def test_empty_list_for_no_appointments() -> None:

    data_store, appointment_service, booked = book_appointment()
    PractitionerService(data_store).register_practitioner('D2', 'John Example', 'Skin')

    no_appointments = appointment_service.list_practitioner_appointments('D2')
    no_match = appointment_service.list_practitioner_appointments('D1', AppointmentStatus.CANCELLED)

    assert no_appointments == []
    assert no_match == []
    assert no_appointments is not no_match
    assert data_store.list_appointments() == [booked]


def test_list_practitioner_appointments_invalid_requests() -> None:

    data_store, appointment_service, booked = book_appointment()

    with pytest.raises(LookupError):
        appointment_service.list_practitioner_appointments('D9')

    with pytest.raises(LookupError):
        appointment_service.list_practitioner_appointments('d1')

    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments(' ')

    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments('D1', 'scheduled')

    assert booked.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [booked]


def test_list_practitioner_appointments_uses_registered_id_and_order() -> None:

    data_store, appointment_service, booked = book_appointment()
    second_appointment = appointment_service.book_appointment('A0', 'P1', 'D1', datetime(2026, 10, 1, 10))

    result = appointment_service.list_practitioner_appointments(' D1 ')

    assert result == [booked, second_appointment]
    assert result[0] is booked
    assert result[1] is second_appointment
    assert result is not data_store.list_appointments()



def test_list_practitioner_appointments_shows_cancelled() -> None:

    data_store, appointment_service, booked = book_appointment()
    appointment_service.cancel_appointment('A1')

    all_appointments = appointment_service.list_practitioner_appointments('D1')
    scheduled_only = appointment_service.list_practitioner_appointments('D1', AppointmentStatus.SCHEDULED)
    cancelled_only = appointment_service.list_practitioner_appointments('D1', AppointmentStatus.CANCELLED)

    assert all_appointments == [booked]
    assert all_appointments[0] is appointment_service.find_appointment('A1')
    assert scheduled_only == []
    assert cancelled_only == [booked]
