import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.services import PractitionerService


def test_find_practitioner_with_valid_id() -> None:
    
    """Verify lookup returns the valid practitioner record."""

    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)
    practitioner = service.register_practitioner('Prac1', 'Joji', 'General')

    assert service.find_practitioner('Prac1') is practitioner
    assert service.find_practitioner(' Prac1 ') is practitioner
    assert data_store.list_practitioners() == [practitioner]


def test_unknown_practitioner_id() -> None:
    """Verify an unknown ID raises LookupError."""

    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)

    with pytest.raises(LookupError):
        service.find_practitioner('Prac3')


def test_invalid_practitioner_id() -> None:
    """Verify an invalid ID is rejected."""

    data_store = SmartCareDataStore()
    service = PractitionerService(data_store)
    practitioner = service.register_practitioner('Prac1', 'Joji', 'General')

    with pytest.raises(ValueError):
        service.find_practitioner(' ')
    with pytest.raises(ValueError):
        service.find_practitioner('')
    with pytest.raises(ValueError):
        service.find_practitioner(None)
    with pytest.raises(ValueError):
        service.find_practitioner(123)

    assert data_store.find_practitioner('Prac1') is practitioner
    assert practitioner.name == 'Joji'
    assert data_store.list_practitioners() == [practitioner]
