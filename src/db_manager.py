import psycopg2
import logging

from src.abs_manager import ABSManager

from src.paths import root_join
from src.config import LOG_LEVEL

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
log_path = root_join('logs', f'{__name__}.log')
fh = logging.FileHandler(log_path, mode='w')
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class DBManager(ABSManager):
    """ Database manager """

    def __init__(self, db_name, params=None):
        """ Connects to Database and creates cursor """
        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """ Returns a list of all companies and the number of vacancies for each company"""
        self.cur.execute(
            """
            SELECT employer_name, COUNT(vacancies.employer_id)
            FROM employers
            INNER JOIN vacancies USING (employer_id)
            GROUP BY employer_name
            ORDER BY COUNT DESC
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """ Returns a list of all vacancies with the company name, job title and salary, and a link to the vacancy."""
        self.cur.execute(
            """
            SELECT v.vacancy_id, e.employer_name, a.name AS area_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            INNER JOIN areas a ON v.vacancy_area = a.area_id
            ORDER BY v.salary DESC
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        """ Returns average salary by vacancies """
        self.cur.execute(
            """
            SELECT AVG(salary)
            FROM vacancies
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """ Returns a list of all vacancies where the salary is higher than the average for all vacancies """
        self.cur.execute(
            """
            SELECT v.vacancy_id, e.employer_name, a.name AS area_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            INNER JOIN areas a ON v.vacancy_area = a.area_id
            WHERE v.salary >= (SELECT AVG(salary) FROM vacancies)
            ORDER BY v.salary DESC
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """ Returns a list of all vacancies whose titles contain the words passed to the method, for example python """
        query = """
            SELECT v.vacancy_id, e.employer_name, a.name AS area_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            INNER JOIN areas a ON v.vacancy_area = a.area_id
            WHERE v.salary >= (SELECT AVG(salary) FROM vacancies)
            """

        q_params = []

        if keyword:
            query += " AND (v.vacancy_name ILIKE %s OR e.employer_name ILIKE %s OR a.name ILIKE %s)"
            q_params.extend([f"%{keyword}%"] * 3)

        query += " ORDER BY v.salary DESC"

        self.cur.execute(query, q_params)
        return self.cur.fetchall()