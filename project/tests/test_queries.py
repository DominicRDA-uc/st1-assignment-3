"""Stage 9 tests for the pure appointment queries.
Covers QRY-01, QRY-02, QRY-03, FP-01, FP-02 and FP-03 using synthetic data.
Appointments are built directly, so no store or service is involved.
"""

from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments


PATIENT = Patient('P1', 'Alex Example')
D1 = Practitioner('D1', 'Taylor Example', 'General')
D2 = Practitioner('D2', 'John Example', 'Skin')


def check_mutation(appointments: list[Appointment]) -> list[tuple]:
    return [
        (a, a.appointment_id, a.practitioner, a.date_time, a.status)
        for a in appointments
    ]


T9 = datetime(2026, 11, 8, 9, 0)
T10 = datetime(2026, 11, 8, 10, 0)
T11 = datetime(2026, 11, 8, 11, 0)


def temp_list() -> list[Appointment]:
    return [
        Appointment('A5', PATIENT, D1, T11, AppointmentStatus.SCHEDULED),
        Appointment('A1', PATIENT, D1, T9, AppointmentStatus.CANCELLED),
        Appointment('A9', PATIENT, D2, T9, AppointmentStatus.SCHEDULED),
        Appointment('A3', PATIENT, D1, T10, AppointmentStatus.COMPLETED),
        Appointment('A6', PATIENT, D1, T9, AppointmentStatus.COMPLETED)
    ]


def test_only_requested_practitioner_is_selected() -> None:
    
    all_appointments = temp_list()

    result = select_appointments(all_appointments, 'D1')

    assert {a.appointment_id for a in result} == {'A1', 'A5', 'A3', 'A6'}
   
    for a in result:
        assert a.practitioner is D1

def test_practitioner_id_is_case_sensitive() -> None:
    
    assert select_appointments(temp_list(), 'd1') == []


def test_default_includes_all_status() -> None:
    
    result = select_appointments(temp_list(), 'D1')

    assert {a.status for a in result} == set(AppointmentStatus)


def test_explicit_status_filters() -> None:
    
    all_appointments = temp_list()
    
    expected = {
        AppointmentStatus.SCHEDULED: ['A5'],
        AppointmentStatus.CANCELLED: ['A1'],
        AppointmentStatus.COMPLETED: ['A3', 'A6'],
    }

    for status, ids in expected.items():
        
        result = select_appointments(all_appointments, 'D1', status)
        for a in result:
            assert a.status is status
            assert a.practitioner is D1
            assert a.appointment_id in ids


def test_no_match_returns_new_empty_list() -> None:
    appt = [Appointment('A1', PATIENT, D1, T9, AppointmentStatus.SCHEDULED)]

    result = select_appointments(appt, 'D1', AppointmentStatus.CANCELLED)

    assert result == []
    assert result is not appt


def test_orders_by_date_time_then_appointment_id() -> None:

    result = select_appointments(temp_list(), 'D1')
    temp_ids = []
    for a in result:
        temp_ids.append(a.appointment_id)

    assert temp_ids == ['A1', 'A6', 'A3', 'A5']


def test_order_and_fields_are_unchanged() -> None:
    appointments = temp_list()
    before_selection = check_mutation(appointments)

    select_appointments(appointments, 'D1')
    select_appointments(appointments, 'D1', AppointmentStatus.SCHEDULED)

    assert check_mutation(appointments) == before_selection
    assert [a.appointment_id for a in appointments] == ['A5', 'A1', 'A9', 'A3', 'A6']


def test_repeated_calls_give_same_result_in_new_list() -> None:
    appointments = temp_list()

    first = select_appointments(appointments, 'D1')
    second = select_appointments(appointments, 'D1')

    assert first == second
    assert first is not second


def test_distinct_list_for_each_input() -> None:
    
    empty_list: list[Appointment] = []
    
    sorted_list = [Appointment('A1', PATIENT, D1, T9, AppointmentStatus.SCHEDULED), 
                   Appointment('A2', PATIENT, D1, T10, AppointmentStatus.SCHEDULED)]
    
    unsorted_list = [Appointment('A2', PATIENT, D1, T10, AppointmentStatus.SCHEDULED), 
                     Appointment('A1', PATIENT, D1, T9, AppointmentStatus.SCHEDULED)]

    for appt_list in (empty_list, sorted_list, unsorted_list):
        before = check_mutation(appt_list)
        result = select_appointments(appt_list, 'D1')
        assert result is not appt_list
        assert check_mutation(appt_list) == before

    result = select_appointments(sorted_list, 'D1')
    assert result == sorted_list

    assert len(result) == len(sorted_list)
    for result_appt, sorted_appt in zip(result, sorted_list):
        assert result_appt is sorted_appt



    result = select_appointments(unsorted_list, 'D1')
    assert len(result) == len(unsorted_list)
    assert result[0] == unsorted_list[1]
    assert result[1] == unsorted_list[0]


def test_named_key_returns_date_time_then_id() -> None:
    
    first_appt = Appointment('A1', PATIENT, D1, T9, AppointmentStatus.SCHEDULED)
    second_appt = Appointment('A2', PATIENT, D1, T9, AppointmentStatus.SCHEDULED)

    assert appointment_sort_key(first_appt) == (T9, 'A1')
    assert appointment_sort_key(second_appt) == (T9, 'A2')

    assert appointment_sort_key(second_appt) > appointment_sort_key(first_appt)


def test_sorting_using_named_key() -> None:
    result = select_appointments(temp_list(), 'D1')

    assert result == sorted(result, key=appointment_sort_key)
    assert result != sorted(result, key=lambda a: a.appointment_id)
    
