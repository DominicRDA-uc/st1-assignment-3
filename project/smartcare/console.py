"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


HEADER = """
=================================================
SMARTCARE
Interactive Console
=================================================
Session data is temporary and will be discarded when you exit.
"""

MENU = """
MAIN MENU
------------------------------------------------------
[1] Register patient
[2] Find patient
[3] Register practitioner
[4] Find practitioner
[5] Book appointment
[6] Cancel appointment
[7] Find appointment
[8] List practitioner appointments
[0] Exit
------------------------------------------------------
"""


def appointment_details(appointment: Appointment) -> str:
    return (
        f'Appointment ID : {appointment.appointment_id}\n'
        f'Patient : {appointment.patient.name} ({appointment.patient.patient_id})\n'
        f'Practitioner : {appointment.practitioner.name} ({appointment.practitioner.practitioner_id})\n'
        f'Specialty : {appointment.practitioner.specialty}\n'
        f'Date/time : {appointment.date_time:%Y-%m-%d %H:%M}\n'
        f'Status : {appointment.status.value.capitalize()}\n'
        f'Reference : {format_appointment(appointment)}'
    )


def parse_status(text: str) -> AppointmentStatus | None:
    """Convert console text to a status.
       Blank means (None) or every status.
      """
    text = text.strip()
    if not text:
        return None
    try:
        return AppointmentStatus(text)
    except ValueError:
        raise ValueError(
            'Status must be scheduled, cancelled or completed',
        ) from None


def run_menu() -> None:
    """
    Runs the register/find/book/cancel/list/exit menu.

    Call services, recover from expected input errors, and keep this
    session's data until exit.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    
    print(HEADER)

    while True:
        print(MENU)
        choice = input('Select an option: ').strip()
        if choice == '0':
            print('Goodbye. Session data discarded.')
            return
        try:
            if choice == '1':
                patient = patients.register_patient(
                    input('Patient ID: '),
                    input('Patient name: '),
                )
                print(f'Patient registered successfully.\nPatient ID : {patient.patient_id}\nName : {patient.name}')
            elif choice == '2':
                patient_id = input('Patient ID: ')
                patient = patients.find_patient(patient_id)
                print(f'Patient found. {patient.patient_id}: {patient.name}')
                print(f'Patient ID : {patient.patient_id}\nName : {patient.name}')
            elif choice == '3':
                practitioner = practitioners.register_practitioner(
                    input('Practitioner ID: '),
                    input('Practitioner name: '),
                    input('Specialty: '),
                )
                print('Practitioner registered successfully.')
                print(f'Practitioner ID : {practitioner.practitioner_id}\nName : {practitioner.name}\nSpecialty : {practitioner.specialty}')
            elif choice == '4':
                practitioner = practitioners.find_practitioner(
                    input('Practitioner ID: '),
                )
                print(f'Practitioner found. {practitioner.practitioner_id}: {practitioner.name}, {practitioner.specialty}')
                print(f'Practitioner ID : {practitioner.practitioner_id}\nName : {practitioner.name}\nSpecialty : {practitioner.specialty}')
            elif choice == '5':
                appointment = appointments.book_appointment(
                    input('Appointment ID: '),
                    input('Patient ID: '),
                    input('Practitioner ID: '),
                    parse_date_time(input('Date/time [YYYY-MM-DD HH:MM]: ')),
                )
                print(f'Appointment booked successfully.\n{appointment_details(appointment)}')
            elif choice == '6':
                appointment = appointments.cancel_appointment(
                    input('Appointment ID: '),
                )
                print(f'Appointment cancelled successfully.\n{appointment_details(appointment)}')
            elif choice == '7':
                appointment = appointments.find_appointment(
                    input('Appointment ID: '),
                )
                print(f'Appointment found.\n{appointment_details(appointment)}')
            elif choice == '8':
                practitioner_id = input('Practitioner ID: ')
                status = parse_status(
                    input('Status filter [scheduled/cancelled/completed, blank = all]: '),
                )
                found = appointments.list_practitioner_appointments(
                    practitioner_id,
                    status,
                )
                practitioner = practitioners.find_practitioner(practitioner_id)
                filter_name = 'All statuses' if status is None else status.value.capitalize()
                print(f'Appointments for {practitioner.name} ({practitioner.practitioner_id})\nFilter: {filter_name}')
                print('-' * 50)
                if not found:
                    print('No appointments found.')
                else:
                    for number, appointment in enumerate(found, 1):
                        print(
                            f'{number}. {appointment.appointment_id}\n'
                            f'Patient : {appointment.patient.name} ({appointment.patient.patient_id})\n'
                            f'Date/time : {appointment.date_time:%Y-%m-%d %H:%M}\n'
                            f'Status : {appointment.status.value.capitalize()}\n'
                            f'Reference : {format_appointment(appointment)}'
                        )
                    print('-' * 50)
                    print(f'{len(found)} appointment{"s" if len(found) != 1 else ""} found.')
            else:
                print('Unknown choice. Choose a number from 0 to 8.')
                
        except (ValueError, LookupError) as error:
            print(f'Error: {error}')
