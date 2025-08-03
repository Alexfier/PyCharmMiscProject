import json
from configparser import ConfigParser, NoSectionError, NoOptionError, MissingSectionHeaderError

import psycopg2
import logging

from src.paths import root_join
from src.config import LOG_LEVEL, TEXT_WIDTH

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = root_join('logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def create_database(database_name: str, params: dict):
    """ Creates a new database and tables within it """

    try:
        logger.info(f"Starting creation of database '{database_name}'")

        # Connect to the default 'postgres' database to create the new database
        # with psycopg2.connect(dbname='postgres', **params) as conn:
        #     conn.autocommit = True
        #     with conn.cursor() as cur:
        #         # Drop the database if it already exists
        #         logger.info(f"Dropping database '{database_name}' if it exists")
        #         cur.execute(f'DROP DATABASE IF EXISTS {database_name};')
        #
        #         # Create the new database
        #         logger.info(f"Creating database '{database_name}'")
        #         cur.execute(f'CREATE DATABASE {database_name};')

        # Connect to the default 'postgres' database to create the new database
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        # Drop the database if it already exists
        logger.info(f"Dropping database '{database_name}' if it exists")
        cur.execute(f'DROP DATABASE IF EXISTS {database_name};')

        # Create the new database
        logger.info(f"Creating database '{database_name}'")
        cur.execute(f'CREATE DATABASE {database_name};')

        # Close the connection to the default 'postgres' database
        cur.close()
        conn.close()

        # Connect to the newly created database
        with psycopg2.connect(dbname=database_name, **params) as conn:
            conn.autocommit = False
            with conn.cursor() as cur:
                # Create table areas
                logger.info("Creating table 'areas'")
                cur.execute(
                    """
                    CREATE TABLE areas (
                        area_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        url TEXT
                    );
                    """
                )

                # Create table employers
                logger.info("Creating table 'employers'")
                cur.execute(
                    """
                    CREATE TABLE employers (
                        employer_id INTEGER PRIMARY KEY,
                        employer_name TEXT NOT NULL,
                        url TEXT,
                        open_vacancies INTEGER
                    );
                    """
                )

                # Create table vacancies
                logger.info("Creating table 'vacancies'")
                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR,
                        vacancy_area INTEGER REFERENCES areas(area_id),
                        salary INTEGER,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        vacancy_url VARCHAR
                    );
                    """
                )

            # Commit the transaction
            conn.commit()

        logger.info(f"Database '{database_name}' and tables created successfully")

    except psycopg2.Error as e:
        logger.error(f"Error creating database '{database_name}': {e}")
        return False

    return True

def save_to_database(areas: dict, employers: dict, vacancies: list, dbname: str, params: dict):
    """ Save data to database """
    try:
        logger.info('Starting to save data to the database')

        with psycopg2.connect(dbname=dbname, **params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:

                logger.info('Saving areas...')

                for area_id, area_data in areas.items():
                    logger.debug(f'Load info from {area_id}.\nData: {area_data}')
                    cur.execute(
                        """
                        INSERT INTO areas (area_id, name, url)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            area_id,
                            area_data.get('name'),
                            area_data.get('url')
                        )
                    )

                logger.info('Saving employers...')

                for employer_id, employer_data in employers.items():
                    logger.debug(f'Load info from {employer_id}.\nData: {employer_data}')
                    cur.execute(
                        """
                        INSERT INTO employers (employer_id, employer_name, url, open_vacancies)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            employer_id,
                            employer_data.get('name'),
                            employer_data.get('url'),
                            employer_data.get('open_vacancies')
                        )
                    )

                logger.info('Saving vacancies...')

                for vacancy_item in vacancies:
                    logger.debug(f'Load info from {vacancy_item.get('id')}.\nData: {vacancy_item}')
                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            vacancy_item.get('id'),
                            vacancy_item.get('name'),
                            vacancy_item.get('area_id'),
                            vacancy_item.get('salary'),
                            vacancy_item.get('employer_id'),
                            vacancy_item.get('url'),
                        )
                    )

                logger.info('Updating open vacancies count...')

                cur.execute(
                    """
                    UPDATE employers
                    SET open_vacancies = subquery.vacancy_count
                    FROM (
                        SELECT employer_id, COUNT (*) as vacancy_count
                        FROM vacancies
                        GROUP BY employer_id
                    ) AS subquery
                    WHERE employers.employer_id = subquery.employer_id
                    """
                )

    except psycopg2.Error as e:
        logger.error(f'Error saving data: {e}')
        return False

    return True


def read_db_config(config_file: str) -> dict[str, str]:
    """ Reads config file and returns params for connection to DB """
    config = ConfigParser()
    try:
        logger.info(f"Reading config file: {config_file}")
        config.read(config_file)

        if 'postgres' not in config:
            raise NoSectionError('postgres')

        db_config = {
            'host': config['postgres'].get('host', ''),
            'port': config['postgres'].get('port', ''),
            'user': config['postgres'].get('user', ''),
            'password': config['postgres'].get('password', '')
        }

        if not all(db_config.values()):
            raise NoOptionError('postgres', 'One or more required options are missing')

        logger.info(f"Successfully read config file: {config_file}")
        return db_config

    except (FileNotFoundError, NoSectionError, NoOptionError, MissingSectionHeaderError) as e:
        logger.error(f'Error reading config file: {e}')
        return {}

def read_employers_list(file_path: str) -> list[int]:
    """ Reads and returns list of integers in specified file """
    try:
        logger.info(f'Reading file: {file_path}')

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, int) for item in data):
                logger.info(f'Successfully read file: {file_path}')

                return data
            else:
                logger.error("Error: JSON file must contain a list of integers.")
                raise ValueError('JSON-file must contain a list of integers')

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        logger.error(f'An error has occurred: {e}')
        return []

def fixed_width(left_text, right_text, replace_char = '-', width = 30):
    """ Align a line of text to a given width with custom padding """
    text_length = len(left_text) + len(right_text)

    fill_length = width - text_length - 2
    if fill_length >= 0:
        formated_text = f'{left_text} {replace_char * fill_length} {right_text}'
        return formated_text
    else:
            return f'{left_text} {replace_char} {right_text}'


def print_vacancy_info(item, unknown: str):
    """ Prints vacancy info """
    print(fixed_width(
        'ID:',
        f'{item[0] if item[0] else unknown}',
        '-',
        TEXT_WIDTH
    ))
    print(fixed_width(
        'Company:',
        f'{item[1] if item[1] else unknown}',
        '-',
        TEXT_WIDTH
    ))
    print(fixed_width(
        'Area:',
        f'{item[2] if item[2] else unknown}',
        '-',
        TEXT_WIDTH
    ))
    print(fixed_width(
        'Vacancy:',
        f'{item[3] if item[3] else unknown}',
        '-',
        TEXT_WIDTH
    ))
    print(fixed_width(
        'Salary from:',
        f'{item[4] if item[4] else unknown}',
        '-',
        TEXT_WIDTH
    ))
    print(fixed_width(
        'URL:',
        f'{item[5] if item[5] else unknown}',
        '-',
        TEXT_WIDTH
    ))
    print('=' * TEXT_WIDTH)


def print_header(text: str):
    """ Prints header """
    print('~' * TEXT_WIDTH)
    print(f'{text}'.center(TEXT_WIDTH, '~'))
    print('~' * TEXT_WIDTH)