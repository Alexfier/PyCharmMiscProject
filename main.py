import os

from src.api_connection import Vacancy
from src.db_connection import (
    create_db,
    create_employers_table,
    create_vacancies_table,
    insert_data_in_employers,
    insert_data_in_vacancies,
)
from src.db_worker import DBManager
from src.utils import select_employers_ids, get_full_employers_info

from dotenv import load_dotenv


load_dotenv()
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


def main():
    """
    Основная функция, связывающая в себе весь функционал проекта и предоставляющая взаимодействие с пользователем
    """
    print(
        """Добро пожаловать в программу для поиска необходимых вакансий из базы данных!
     Вам необходимо выбрать не менее 10 интересующих вас работодателей"""
    )
    employers_ids = select_employers_ids()

    print("""Работодатели успешно выбраны""")
    vacancies = Vacancy()
    vacancies_list = []
    employers_with_vacancies = []

    for employer in employers_ids:
        new_vacancies = vacancies._connection(employer)
        if new_vacancies:
            vacancies_list.extend(new_vacancies)
            employers_with_vacancies.append(employer)

    if not employers_with_vacancies:
        print("Нет доступных вакансий у выбранных работодателей.")

    else:

        db_name = input("Создадим базу данных. Введите название: ")
        params = {
            "host": "localhost",
            "port": "5432",
            "database": "postgres",
            "user": "maria_zhiganova",
            "password": DATABASE_PASSWORD,
        }

        create_db(params, db_name)

        print("""Создаем необходимые таблицы...""")
        create_employers_table(params, db_name)
        create_vacancies_table(params, db_name)

        print("Заполняем таблицу необходимыми данными...")
        full_employers_info = get_full_employers_info(employers_ids)
        insert_data_in_employers(params, db_name, full_employers_info)
        print(vacancies_list)
        insert_data_in_vacancies(params, db_name, vacancies_list)

        db_option = DBManager("localhost", db_name, "maria_zhiganova", DATABASE_PASSWORD)

        while True:
            print(
                """
            1. Показать компании и количество вакансий
            2. Показать все вакансии
            3. Показать среднюю зарплату
            4. Показать вакансии с зарплатой выше средней
            5. Показать вакансии по ключевому слову"""
            )

            option = input("Выберите опцию (или введите 'exit' для выхода): ")

            if option == "exit":
                break

            elif option == "1":
                content = db_option.get_companies_and_vacancies_count()
                for x in content:
                    print(f"""Company - {x[0]}: {x[1]} vacancies""")

            elif option == "2":
                content = db_option.get_all_vacancies()
                for x in content:
                    print(
                        f"""Vacancy: {x[0]}
                            Salary: {x[2]}
                            Company: {x[1]}
                            URL: {x[3]}"""
                    )

            elif option == "3":
                content = db_option.get_avg_salary()
                for x in content:
                    print(f"""Average salary: {x[0]}""")

            elif option == "4":
                content = db_option.get_vacancies_with_higher_salary()
                for x in content:
                    print(
                        f"""Vacancy: {x[1]}
                            id: {x[0]}
                            description: {x[2]}
                            salary from {x[3]}
                            published at {x[4]}
                            url: {x[6]}"""
                    )

            elif option == "5":
                keyword = input("Введите ключевое слово для поиска по вакансиям: ")
                content = db_option.get_vacancies_with_keyword(keyword)
                for x in content:
                    print(
                        f"""Vacancy: {x[1]}
                            id: {x[0]}
                            description: {x[2]}
                            salary from {x[3]}
                            published at {x[4]}
                            url: {x[6]}"""
                    )

            else:
                print("Некорректный ввод. Пожалуйста, попробуйте снова.")

        db_option.close_connection()


if __name__ == "__main__":
    main()