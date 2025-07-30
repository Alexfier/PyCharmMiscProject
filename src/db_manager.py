from typing import List, Optional

import psycopg2


class DBManager:
    """Класс для управления данными в базе данных PostgreSQL"""

    def __init__(self, db_params: dict) -> None:
        self.conn = psycopg2.connect(**db_params)

    def __del__(self) -> None:
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> List[tuple]:
        """Получение списка всех компаний и количества вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    employers.name,
                    LEFT(employers.industry, 100) AS industry_short,
                    COUNT(vacancies.vacancy_id) AS vacancies_count
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                GROUP BY employers.employer_id, employers.name, employers.industry
                ORDER BY vacancies_count DESC
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> List[tuple]:
        """Получение списка всех вакансий с указанием компании, названия, зарплаты и ссылки"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    employers.name AS company_name,
                    vacancies.title AS vacancy_title,
                    vacancies.salary_from,
                    vacancies.salary_to,
                    vacancies.currency,
                    vacancies_url AS vacancy_url
                FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                ORDER BY company_name, vacancy_title
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """Получение средней зарплаты по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    AVG((COALESCE(vacancies.salary_from, vacancies.salary_to) +
                    COALESCE(vacancies.salary_to, vacancies.salary_from))/2) AS average_salary
                FROM vacancies
                WHERE
                    vacancies.salary_from IS NOT NULL OR
                    vacancies.salary_to IS NOT NULL
            """
            )
            result = cur.fetchone()
            return result[0] if result else  None

    def get_vacancies_with_higher_salary(self) -> List[tuple]:
        """Получение списка вакансий выше средней"""
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    employers.name AS company_name,
                    vacancies.title AS vacancy_title,
                    vacancies.salary_from,
                    vacancies.salary_to,
                    vacancies.currency,
                    vacancies.url AS vacancy_url
                FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE
                    (COALESCE(vacancies.salary_from, vacancies.salary_to) +
                    COALESCE(vacancies.salary_to, vacancies.salary_from)) / 2 ) > %s
                ORDER BY
                    ((COALESCE(vacancies.salary_from, vacancies.salary_to) +
                    COALESCE(vacancies.salary_to, vacancies.salary_from)) / 2 ) DESC
            """,
                (avg_salary,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[tuple]:
        """Получение списка вакансий по ключевому слову"""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    employers.name AS company_name,
                    vacancies.title AS vacancy_title,
                    vacancies.salary_from,
                    vacancies.salary_to,
                    vacancies.currency,
                    vacancies.url AS vacancies_url
                FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                WHERE LOWER(vacancies.title) LIKE LOWER(%s)
                ORDER BY company_name, vacancy_title
            """,
                (f'%{keyword}%',),
            )
            return cur.fetchall()