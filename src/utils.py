from typing import Dict, List

from src.api_connection import EmployerHH, Vacancy


def select_employers_ids() -> list:
    """
    Вспомогательная функция для выбора интересующих работодателей по ключевому слову
    """
    employers_id = []

    while len(employers_id) < 10:
        keyword = input("Введите ключевое слово для поиска работодателей: ")
        data = EmployerHH()
        search_results = data.get_employer_ids(keyword)

        if not search_results:
            print("Работодатели не найдены. Попробуйте другое ключевое слово.")
            continue

        print("Найдены следующие работодатели:")
        for idx, employer in enumerate(search_results):
            for employer_id, employer_name in employer.items():
                print(f"{idx + 1}. ID: '{employer_id}', Название: '{employer_name}'")

        selected_ids = input(
            "Введите номера работодателей для добавления в список (через запятую): "
        )

        selected_indices = selected_ids.split(",")
        for index in selected_indices:
            try:
                index = int(index.strip()) - 1
                if 0 <= index < len(search_results):
                    employer_id = list(search_results[index].keys())[0]
                    if employer_id not in employers_id:
                        vacancies = Vacancy()._connection(employer_id)
                        if vacancies:
                            employers_id.append(employer_id)
                            print(f"Работодатель с ID {employer_id} добавлен.")
                        else:
                            print(
                                f"Работодатель с ID {employer_id} не имеет вакансий и не будет добавлен."
                            )
                    else:
                        print(f"Работодатель с ID {employer_id} уже добавлен.")
                else:
                    print(
                        f"Неверный номер: {index + 1}. Пожалуйста, выберите номер из списка."
                    )
            except ValueError:
                print(
                    f"Некорректный ввод: {index}. Пожалуйста, введите номера через запятую."
                )

        if len(employers_id) < 10:
            print(
                "У вас недостаточно работодателей с вакансиями. Пожалуйста, добавьте больше."
            )
            print(f"Текущий список выбранных работодателей: {employers_id}")
        else:
            print(
                "Вы успешно выбрали достаточное количество работодателей с вакансиями."
            )

    return employers_id


def get_full_employers_info(employer_ids: List[int]) -> Dict[int, Dict]:
    """
    Вспомогательная функция для получения информации о работодателях по их ID.
    """
    employer_info_dict = {}
    employers = EmployerHH()

    for employer_id in employer_ids:
        info = employers.get_employer_info(employer_id)
        if info:
            employer_info_dict[employer_id] = info
        else:
            print(f"Информация о работодателе с ID {employer_id} не найдена.")
            employer_info_dict[employer_id] = {}

    return employer_info_dict