from abc import ABC, abstractmethod
from typing import Any, Optional, Dict

import requests


class BaseParser(ABC):
    """
    Базовый класс для создания классов для подключения к АПИ с методом подключения
    """
    def __init__(self):
        self.base_url = "https://api.hh.ru/"

    @abstractmethod
    def _connection(self, *args):
        pass


class EmployerHH(BaseParser):
    """
    Класс для работы с API HeadHunter.
    """

    def _connection(self, keyword: str) -> list:
        """
        Метод, который подключается к API hh.ru и получает работодателей по ключевому слову.
        """
        url = f"{self.base_url}employers?text={keyword}&page=0&per_page=100"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")
            return []

    def get_employer_ids(self, keyword: str) -> list[dict[Any, Any]] | None:
        employers = self._connection(keyword)

        ids = []
        for employer in employers:
            data = {employer["id"]: employer["name"]}
            ids.append(data)
        if ids:
            return ids
        else:
            print("Айди не найдены")

    def get_employer_info(self, employer_id: int) -> Optional[Dict]:
        """
        Метод для получения информации о работодателе по его ID.
        """
        url = f"{self.base_url}employers/{employer_id}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Не удалось получить информацию о работодателе {employer_id}. Причина: {response.reason}"
            )
            return None


class Vacancy(BaseParser):
    """
    Класс для работы с API HeadHunter.
    """

    def _connection(self, employer_id: int) -> None | list:
        """
        Метод, который подключается к апи hh.ru и получает вакансии по айди работодателя в формате json словарей
        """
        url = f"{self.base_url}vacancies?employer_id={employer_id}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()["items"]

        else:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")
            return []