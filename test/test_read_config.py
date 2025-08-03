from pathlib import Path


from src.utils import read_db_config


def test_read_db_config_success(temp_config_file):
    expected_config = {
        'host': 'localhost',
        'port': '5432',
        'user': 'test_user',
        'password': 'test_password'
    }
    assert read_db_config(temp_config_file) == expected_config

# Тест на отсутствие файла
def test_read_db_config_file_not_found():
    non_existent_file = "non_existent_file.ini"
    assert read_db_config(non_existent_file) == {}

# Тест на отсутствие секции
def test_read_db_config_no_section(temp_config_file):
    config_content = """
    [wrong_section]
    host = localhost
    port = 5432
    user = test_user
    password = test_password
    """
    config_file = Path(temp_config_file)
    config_file.write_text(config_content)
    assert read_db_config(temp_config_file) == {}

# Тест на отсутствие ключа
def test_read_db_config_no_option(temp_config_file):
    config_content = """
    [postgres]
    host = localhost
    port = 5432
    user = test_user
    """
    config_file = Path(temp_config_file)
    config_file.write_text(config_content)
    assert read_db_config(temp_config_file) == {}

# Тест на пустой файл
def test_read_db_config_empty_file(temp_config_file):
    config_file = Path(temp_config_file)
    config_file.write_text("")
    assert read_db_config(temp_config_file) == {}

# Тест на неправильный формат файла
def test_read_db_config_invalid_format(temp_config_file):
    config_content = """
    [postgres
    host = localhost
    port = 5432
    user = test_user
    password = test_password
    """
    config_file = Path(temp_config_file)
    config_file.write_text(config_content)
    assert read_db_config(temp_config_file) == {}