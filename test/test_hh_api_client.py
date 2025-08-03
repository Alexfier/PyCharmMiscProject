import pytest

from src.hh_api_client import HHAPIClient

def test_valid_id():
    """ Test valid id method """
    assert HHAPIClient.valid_id(12345) == 12345
    with pytest.raises(ValueError, match='Invalid employer ID'):
        HHAPIClient.valid_id(-1)
    with pytest.raises(ValueError, match='Invalid employer ID'):
        HHAPIClient.valid_id('invalid')

def test_check_existence(mock_requests):
    """ Test check existence method"""
    assert HHAPIClient.check_existence(12345) is True
    with pytest.raises(ValueError, match=''):
        HHAPIClient.check_existence(99999)

def test_load_vacancy_by_emp_id(mock_requests, hh_api_client):
    """Test load_vacancy_by_emp_id method."""
    hh_api_client.load_vacancy_by_emp_id(12345)
    assert len(hh_api_client.get_info()) == 1
    assert hh_api_client.get_info()[0]['id'] == 1
    assert hh_api_client.get_info()[0]['name'] == 'Test Vacancy'


def test_load_vacancies_by_emp_ids(mock_requests, hh_api_client):
    """Test load_vacancies_by_emp_ids method."""
    hh_api_client.load_vacancies_by_emp_ids([12345, 67890])
    assert len(hh_api_client.get_info()) == 2
    assert hh_api_client.get_info()[0]['id'] == 1
    assert hh_api_client.get_info()[0]['name'] == 'Test Vacancy'
    assert hh_api_client.get_info()[1]['id'] == 1
    assert hh_api_client.get_info()[1]['name'] == 'Test Vacancy'

def test_load_vacancy_by_emp_id_invalid(mock_requests, hh_api_client):
    """Test load_vacancy_by_emp_id method with invalid employer_id."""
    with pytest.raises(ValueError, match='Employer ID does not exist'):
        hh_api_client.load_vacancy_by_emp_id(99999)

def test_load_vacancies_by_emp_ids_invalid(mock_requests, hh_api_client):
    """Test load_vacancies_by_emp_ids method with invalid employer_id."""
    with pytest.raises(ValueError, match='Employer ID does not exist'):
        hh_api_client.load_vacancies_by_emp_ids([12345, 99999])