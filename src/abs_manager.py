from abc import ABC, abstractmethod

class ABSManager(ABC):
    def get_companies_and_vacancies_count(self):
        """ Returns a list of all companies and the number of vacancies for each company"""

    def get_all_vacancies(self):
        """ Returns a list of all vacancies with the company name, job title and salary, and a link to the vacancy."""

    def get_avg_salary(self):
        """ Returns average salary by vacancies """

    def get_vacancies_with_higher_salary(self):
        """ Returns a list of all vacancies where the salary is higher than the average for all vacancies """

    def get_vacancies_with_keyword(self, keyword: str):
        """ Returns a list of all vacancies whose titles contain the words passed to the method, for example python """