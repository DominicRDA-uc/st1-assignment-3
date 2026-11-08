"""Stage 9 integrated service workflow test using synthetic data."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

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


def run_menu(lines: list[str]) -> str:
    """Run the real menu program with scripted input and return its output."""
    
    result = subprocess.run(
        [sys.executable, 'main.py', '--interactive'],
        input='\n'.join(lines)+'\n',
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    return result.stdout


def test_UI_01_menu_workflow() -> None:
    """UI-01: full menu sequence in one session."""
    
    output = run_menu([
        '1', 'P1', 'Alex Example',
        '3', 'D1', 'Taylor Example', 'General',
        '3', 'D2', 'John Example', 'Skin',
        '2', 'P1',
        '4', 'D1',
        '4', 'D2',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '5', 'A3', 'P1', 'D1', '2026-10-01 09:00',
        '5', 'A2', 'P1', 'D2', '2026-10-01 09:00',
        '6', 'A1',
        '7', 'A1',
        '8', 'D1', '',
        '8', 'D1', 'scheduled',
        '5', 'A4', 'P1', 'D1', '2026-10-01 09:00',
        '8', 'D1', '',
        '0',
    ])

    assert 'Error: Practitioner already has a SCHEDULED appointment' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'No appointments found.' in output
    assert 'A4: P1 with D1, 2026-10-01 09:00, scheduled' in output
    assert 'Goodbye. Session data discarded.' in output


def test_UI_02_menu_recovers_from_invalid_input() -> None:
    """UI-02: each rejection is reported and the menu continues."""
    
    output = run_menu([
        '99',
        '2', ' ',
        '2', 'P9',
        '1', 'P1', 'Alex Example',
        '1', 'P1', 'Alex Example',
        '3', 'D1', 'Taylor Example', 'General',
        '5', 'A1', 'P9', 'D1', '2026-10-01 09:00',
        '5', 'A1', 'P1', 'D9', '2026-10-01 09:00',
        '5', 'A1', 'P1', 'D1', '2026-10-01 9:00',
        '5', 'A1', 'P1', 'D1', '2026-02-30 09:00',
        '7', 'A1',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '6', 'A1',
        '6', 'A1',
        '6', 'A9',
        '8', 'D1', 'booked',
        '7', 'A1',
        '0',
    ])

    assert 'Unknown choice. Choose a number from 0 to 8.' in output
    assert 'Error: Patient ID cannot be blank' in output
    assert 'Error: Patient not found' in output
    assert 'Error: Patient ID already exists' in output
    assert 'Error: Practitioner not found' in output
    assert 'Error: Use date/time format YYYY-MM-DD HH:MM' in output
    assert 'Error: Invalid calendar date/time' in output
    assert 'Error: Appointment not found' in output
    assert 'Error: Only SCHEDULED appointments may be cancelled' in output
    assert 'Error: Status must be scheduled, cancelled or completed' in output
    assert 'Appointment booked successfully.' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, scheduled' in output
