"""Checks of patient search through PatientService."""

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import PatientService


def test_find_patient_with_valid_id() -> None:
    """Verify lookup returns the valid patient record."""

    data_store = SmartCareDataStore()
    service = PatientService(data_store)
    patient = service.register_patient('J1', 'Joji')

    assert service.find_patient('J1') is patient
    assert service.find_patient(' J1 ') is patient
    assert data_store.list_patients() == [patient]


def test_unknown_patient_id() -> None:
   
    """Verify an unknown ID raises LookupError"""
   
    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    with pytest.raises(LookupError):
        service.find_patient('J3')
    

def test_invalid_patient_id() -> None:
    
    """Verify an invalid ID is rejected"""

    data_store = SmartCareDataStore()
    service = PatientService(data_store)

    patient = service.register_patient('J1', 'Joji')

    with pytest.raises(ValueError):
        service.find_patient(' ')
    with pytest.raises(ValueError):
        service.find_patient('')
    with pytest.raises(ValueError):
        service.find_patient(None)
    with pytest.raises(ValueError):
        service.find_patient(123)

    assert data_store.find_patient('J1') is patient
    assert patient.name == 'Joji'
    assert data_store.list_patients() == [patient]
