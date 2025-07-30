from typing import Dict, List

import psycopg2


def create_database(params: dict, db_name: str) -> None:
    """Создание базы данных"""
    conn = None
    try:
        # Подключаемся
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        # Формирование запроса
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS {db_name}')  # Удаляем БД
            cur.execute(f'CREATE DATABASE {db_name}')  # Создаем БД
        print(f'База "{db_name}" успешно пересоздана!')

    except psycopg2.Error as e:
        print(f'Ошибка при создании БД: {e}')
        raise

    finally:
        if conn:
            conn.close()  # закрываем соединение


def create_tables(conn) -> None:
    """Создаем таблицу employers и vacancies в базе данных"""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                    employer_id VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    industry TEXT,
                    url VARCHAR(255)
                )
            """
            )
            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_id VARCHAR(20) PRIMARY KEY,
                    employer_id VARCHAR(20) REFERENCES employers(employer_id),
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    url VARCHAR(255)
                )
            """
            )
        conn.commit()
        print("Таблицы 'employers' и 'vacancies' успешно созданы.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f'Ошибка при создании таблицы: {e}')
        raise


def save_employer_to_db(conn, employer: Dict) -> None:
    """Сохранение данных в таблицу работодателя"""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, industry, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING
            """,
                (
                    employer['id'],
                    employer['name'],
                    ', '.join([ind['name'] for ind in employer.get('industries', [])]),
                    employer['alternate_url'],
                ),
            )
        conn.commit()
        print(f"Работодатель '{employer['name']}' сохранен в БД > 'employers'.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка при создании работодателя {employer.get('name')}: {e}")
        raise


def save_vacancies_to_db(conn, vacancies: List[Dict], employer_id: str) -> None:
    """Сохранение списков вакансий в таблицу vacancies"""
    try:
        with conn.cursor() as cur:
            for vacancy in vacancies:
                employer_name = vacancy.get('employer', {}).get('name')
                salary = vacancy.get('salary')
                salary_from = salary.get('from') if salary else None
                salary_to = salary.get('to') if salary else None
                currency = salary.get('currency') if salary else None

                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, employer_id, title, description, salary_from, salary_to, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                    """,
                    (
                        vacancy['id'],
                        employer_id,
                        vacancy['name'],
                        vacancy.get('description', ''),
                        salary_from,
                        salary_to,
                        currency,
                        vacancy['alternate_url'],
                    ),
                )
        conn.commit()
        print(
            f"Сохранено {len(vacancies)} вакансий для работодателя '{employer_name}' в БД > 'vacancies'"
        )

    except psycopg2.Error as e:
        conn.rellback()
        print(f'Ошибка при сохранении вакансии: {e}')
        raise