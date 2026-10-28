from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
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
    
    appointment_service.book_appointment('A1','P1','D1',datetime(2026, 10, 1, 9))
    
    return data_store, appointment_service


def test_cancel_appointment_with_valid_id() -> None:
    
    data_store, appointment_service = book_appointment()

    appointment = appointment_service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment_service.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]


def test_unknown_appointment_id() -> None:

    data_store, appointment_service = book_appointment()

    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A3')


def test_invalid_transition_appointment() -> None:

    data_store, appointment_service = book_appointment()
    
    appointment = appointment_service.cancel_appointment('A1')

    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]
