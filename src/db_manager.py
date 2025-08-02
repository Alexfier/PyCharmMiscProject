import psycopg2


def create_db(params: dict, db_name: str) -> None:
    """
    Функция для создания БД
    """
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE {db_name};")

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


def create_employers_table(params: dict, db_name: str) -> None:
    """
    Функция для создания таблицы сотрудников
    """
    params["database"] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS employers (
                        id SERIAL PRIMARY KEY,
                        employer_id VARCHAR UNIQUE,
                        name VARCHAR NOT NULL,
                        url VARCHAR,
                        open_vacancies INTEGER
                    );
                """
                )
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def create_vacancies_table(params: dict, db_name: str) -> None:
    """
    Функция для создания таблицы вакансий
    """
    params["database"] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        description TEXT,
                        salary INTEGER,
                        published_at DATE,
                        employer_id VARCHAR NOT NULL,
                        CONSTRAINT fk_employer_id FOREIGN KEY(employer_id) 
                        REFERENCES employers(employer_id) ON DELETE CASCADE,
                        url VARCHAR NOT NULL
                    );
                """
                )
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def insert_data_in_vacancies(params: dict, db_name: str, data: list) -> None:
    """
    Функция для заполнения таблицы вакансий
    """
    params["database"] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                for v in data:
                    salary = None
                    if v.get("salary") is not None:
                        salary = v["salary"].get("from", None)
                    cur.execute(
                        """INSERT INTO vacancies (name, description, salary, employer_id, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                        (
                            v["name"],
                            v.get("responsibility", "Нет описания"),
                            salary,
                            v["employer"]["id"],
                            v["alternate_url"],
                        ),
                    )
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при заполнении таблицы: {e}")


def insert_data_in_employers(params: dict, db_name: str, data: dict) -> None:
    """
    Функция для заполнения таблицы сотрудников
    """
    params["database"] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                for employer_id, employer_info in data.items():
                    if isinstance(employer_info, dict) and employer_info:
                        open_vacancies = employer_info.get("open_vacancies", 0)
                        name = employer_info.get("name", "Неизвестно")
                        url = employer_info.get("url", "")

                        cur.execute(
                            """INSERT INTO employers (employer_id, name, url, open_vacancies)
                                       VALUES (%s, %s, %s, %s)
                                       """,
                            (employer_id, name, url, open_vacancies),
                        )
                    else:
                        print(
                            f"Неверный формат данных для работодателя {employer_id}: {employer_info}"
                        )
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при заполнении таблицы: {e}")