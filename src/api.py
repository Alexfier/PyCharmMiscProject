from http.client import responses
from typing import Optional, Dict, List

import requests


class HeadHunterApi:
    """Класс для взаимодействия с Api hh.ru для получения данных
    о работодателе и вакансиях"""

    def __init__(self) -> None:
        self.base_url = 'https://api.hh.ru/'
        self.headers = {'User-Agent': 'HH-User-Agent'}

    def get_employer(self, employer_id: str) -> Optional[Dict]:
        """Получение данных о работодателе по его ID"""
        url = f'{self.base_url}employers/{employer_id}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        print(f'Получение данных о работодателе "{response.json()['name']}".')
        return response.json() if response.status_code == 200 else None

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        """Получение списка вакансий работодателя по его ID"""
        vacancies = []
        page = 0  # первая страница
        pages = 1  # Конечня страница

        while page < pages:
            params = {'employer_id': employer_id, 'page': page, 'per_page': 100}

            response = requests.get(
                f'{self.base_url}vacancies', headers=self.headers, params=params
            )
            response.raise_for_status()
            data = response.json()
            vacancies.extend(data['items'])
            pages = data['pages']
            page += 1
        return vacancies


