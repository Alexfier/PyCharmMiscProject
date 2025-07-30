import os

import psycopg2
from dotenv import load_dotenv

from src.db_manager import DBManager
from src.api import HeadHunterApi
from src.saver import create_database, save_employer_to_db, create_tables, save_vacancies_to_db


def main() -> None:
    """Собираем данные о работодателях и вакансиях с HH.ru в юазу данных"""
    # Подключение к БД
    load_dotenv()
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': 'postgres',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    db_name = os.getenv('DB_NAME')

    # # Закрыть все активные сессии
    # connection = psycopg2.connect(database='postgres', user='DB_USER', password='DB_PASSWORD', host='DB_HOST')
    # connection.autocommit = True
    # cursor = connection.cursor()
    # cursor.execute("""
    #     SELECT pg_terminate_backend(pg_stat_activity.pid)
    #     FROM pg_stat_activity
    #     WHERE pg_stat_activity.datame = 'test'
    #       AND pid <> pg_backend_pid();
    # """)
    # cursor.close()
    # connection.close()

    # Создание БД
    create_database(db_params, db_name)
    db_params['database'] = db_name

    # Подключение к БД и создание таблиц
    conn = psycopg2.connect(**db_params)
    create_tables(conn)

    # Загрузка данных
    hh_api = HeadHunterApi()
    with open('employer_id.text', 'r') as f:
        employer_id = [line.strip() for line in f]

        for employer in employer_id:
            emp = hh_api.get_employer(employer)
            if emp:
                save_employer_to_db(conn, emp)
                vacancies = hh_api.get_vacancies(employer)
                save_vacancies_to_db(conn, vacancies, employer)

        conn.close()


def user_interaction() -> None:
    """Интерфейс взаимодействия с пользователем"""
    # Подключение к БД
    load_dotenv()
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': 'postgres',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    db_manager = DBManager(db_params)

    while True:
        print(
            """
            Меню действий
    1. Список компаний и вакансий
    2. Список всех вакансий
    3. Средняя зарплата
    4. Вакансия с зарплатой выше средней
    5. Поиск по ключевому слову
    6. Выход
            """
        )

        value = input('> ').strip()

        if value == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            for company, industry, count in companies:
                points = '...' if len(industry) >= 40 else ''
                print(f'{company}: {count} вакансий\n{industry}{points}\n')

        elif value == '2':
            vacancies = db_manager.get_all_vacancies()
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = ''
                if salary_from or salary_to:
                    salary = f'Зарплата {salary_from or '-'} - {salary_to or '-'} {currency}'
                print(f'{company} | {title} | {salary} | {url}')

        elif value == '3':
            vacancies = db_manager.get_avg_salary()
            print(f'Средняя зарплата: {.2}')

        elif value == '4':
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = f'Зарплата: {salary_from} - {salary_to} {currency}'
                print(f'{company} | {title} | {salary} | {url}')

        elif value == '5':
            keyword = input('Введите ключевое слово: ').strip()
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for company, title, salary_from, salary_to, currency, url in vacancies:
                salary = ''
                if salary_from or salary_to:
                    salary = f'Зарплата {salary_from or '-'} - {salary_to or '-'} {currency}'
                print(f'{company} | {title} | {salary} | {url}')

        elif value == '0':
            break
        else:
            print('Неверный ввод. Попробуйте снова.')


if __name__ == "__main__":
    main()
    user_interaction()