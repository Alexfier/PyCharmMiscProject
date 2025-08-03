import logging

from src.config import LOG_LEVEL, TEXT_WIDTH
from src.db_manager import DBManager
from src.hh_api_client import HHAPIClient
from src.paths import root_join
from src.utils import read_employers_list, read_db_config, create_database, save_to_database, fixed_width, \
    print_vacancy_info, print_header

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = root_join('logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

commands = [
    ("EXT", "Exit the program"),
    ("CVCOUNT", "Get a list of all companies and the number of vacancies for each company"),
    ("GETALL", "Get a list of all vacancies with the company name, job title and salary and a link to the vacancy"),
    ("AVGSAL", "Get average salary for vacancies"),
    ("HIAVG", "Get a list of all vacancies where the salary is higher than the average for all vacancies"),
    ("KEYW", "Get a list of all vacancies whose titles contain the words passed to the method, for example python")
]

def main() -> bool:
    """ Main function """
    logger.info('The program has been launched')
    try:
        config_path = root_join('data', 'config.ini')
        logger.info(f'Getting params from {config_path}')

        params = read_db_config(config_path)
        logger.info('Params successfully received')

        # Creating DB
        db_name = 'vacancies'
        logger.info(f'Creating database {db_name}')
        create_database(db_name, params)

        # Get a list of saved employers to work with
        emp_ids_path = root_join('data', 'employer_ids.json')
        logger.info(f'Reading employers ids from {emp_ids_path}')

        employers_list = read_employers_list(emp_ids_path)
        logger.info(f'IDs is {employers_list}')

        # Creating HH API Client
        logger.info('Creating hh.ru API Client')
        hh_client = HHAPIClient()

        # Loading vacancies from hh.ru
        logger.info('Loading vacancies from employers')
        hh_client.load_vacancies_by_emp_ids(employers_list)

        # Getting data
        logger.info('Getting areas...')
        areas = hh_client.get_areas()

        logger.info('Getting employers...')
        employers = hh_client.get_employers()

        logger.info('Getting vacancies...')
        vacancies = hh_client.get_vacancies()

        # Inserting data to database
        logger.info('Inserting data to Database...')
        save_to_database(areas, employers, vacancies, db_name, params)

        # Creating db_manager
        logger.info('Creating DBManager instance')
        db_manager = DBManager(db_name, params)

    except Exception as e:
        logger.error(f'An error has occurred: {e}')
        return False

    while True:
        print("Please enter the following characters to:")
        for command in commands:
            print(fixed_width(
                f"'{command[0]}'",
                f"{command[1]}",
                '-',
                TEXT_WIDTH
            ))
        user_input = input()

        # Exit program
        if user_input.lower() == 'ext':
            logger.info('Terminating the program')
            return True

        # Vacancies count
        elif user_input.lower() == 'cvcount':
            vacancies_count = db_manager.get_companies_and_vacancies_count()
            print_header('NUMBER OF VACANCIES FOR EACH EMPLOYER:')
            for item in vacancies_count:
                print('=' * TEXT_WIDTH)

                print(fixed_width(
                    f'Employer: {item[0]}',
                    f'Vacancies: {item[1]}',
                    '-',
                    TEXT_WIDTH
                ))

                print('=' * TEXT_WIDTH)

        # Getting all
        elif user_input.lower() == 'getall':
            all_vacancies = db_manager.get_all_vacancies()
            print_header('ALL FOUND VACANCIES:')
            for item in all_vacancies:
                print_vacancy_info(item, '~Unknown~')

        elif user_input.lower() == 'avgsal':
            avg_sal = db_manager.get_avg_salary()
            print('=' * TEXT_WIDTH)
            print(f'Average salary: {avg_sal}')
            print(fixed_width(
                'Average salary:',
                f'{round(avg_sal[0][0]) if avg_sal[0][0] else '-Unknown-'}',
                '-',
                TEXT_WIDTH
            ))
            print('=' * TEXT_WIDTH)

        elif user_input.lower() == 'hiavg':
            higher_than_avg_vacancies = db_manager.get_vacancies_with_higher_salary()
            print_header('FOUND VACANCIES WITH SALARY THAT HIGHER THAN AVERAGE:')
            for item in higher_than_avg_vacancies:
                print_vacancy_info(item, '~Unknown~')

        elif user_input.lower() == 'keyw':
            keyword = input('Enter your keyword: ')
            keyw_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print_header('FOUND VACANCIES WITH YOUR KEYWORD:')
            for item in keyw_vacancies:
                print_vacancy_info(item, '~Unknown~')
        else:
            print('Your request is not provided, please enter another request')


if __name__ == '__main__':
    main()