import json
import os.path

from src.utils import read_employers_list

def test_read_emp_list_success(temp_json_file):
    expected_data = [1, 2, 3, 4, 5]
    assert read_employers_list(temp_json_file) == expected_data


def test_read_emp_list_file_not_found():
    non_existed_dile = 'non_existed_file.json'
    assert read_employers_list(non_existed_dile) == []


def test_read_emp_list_invalid_json(tmp_path):
    invalid_data = 'invalid json data'
    file_path = os.path.join(tmp_path, 'invalid.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(invalid_data)
    assert read_employers_list(file_path) == []

def test_read_json_file_invalid_data(tmp_path):
    invalid_data = ["1", "2", "3"]
    file_path = tmp_path / "invalid_data.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(invalid_data, file)
    assert read_employers_list(str(file_path)) == []