from typing import Any

import psycopg2


class DBManager:
    def __init__(self, host: str, database: str, user: str, password: str) -> None:
        """
        Инициализация класса DBManager и установка соединения с БД.
        """
        try:
            self.connection = psycopg2.connect(
                host=host, database=database, user=user, password=password
            )
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к БД: {e}")

    def close_connection(self) -> None:
        """Закрытие соединения с БД."""
        if self.connection:
            self.connection.close()

    def get_companies_and_vacancies_count(self) -> None | list[Any]:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """SELECT e.name, COUNT(v.id) AS vacancy_count 
                    FROM employers e
                    LEFT JOIN vacancies v USING(employer_id)
                    GROUP BY e.name;
                    """
                )
                data = cursor.fetchall()
                if data:
                    return data

        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
            return []

    def get_all_vacancies(self) -> None | list:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """SELECT v.name AS vacancy_name, e.name AS company_name, v.salary, v.url 
                    FROM vacancies v
                    LEFT JOIN employers e USING(employer_id);
                    """
                )
                data = cursor.fetchall()
                if data:
                    return data

        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
            return []

    def get_avg_salary(self) -> None | list[Any]:
        """
        Получает среднюю зарплату по вакансиям.
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    """
                  SELECT ROUND(AVG(salary)) FROM vacancies;"""
                )
                data = cur.fetchall()
                if data:
                    return data

        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
            return []

    def get_vacancies_with_higher_salary(self) -> None | list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    """SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                """
                )
                data = cur.fetchall()
                if data:
                    return data

        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str) -> None | list:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        try:
            with self.connection.cursor() as cur:
                cur.execute(
                    """SELECT * FROM vacancies
                WHERE name LIKE %s;
                """,
                    (f"%{keyword}%",),
                )
                data = cur.fetchall()
                if data:
                    return data

        except psycopg2.Error as e:
            print(f"Ошибка при получении данных: {e}")
            return []