# Интерпретатор python для запуска проверок кода в контейнере 

![Language](https://img.shields.io/badge/language-Python-blue.svg)


## Основные функции

- Запуск Python-кода в Docker-контейнере.
- Проверка кода с заранее заданными входными данными.

## Требования

- **Docker**: для создания и управления контейнерами.
- **Python 3.11**: для выполнения Python-кода.

<details>
<summary>
  <strong>
    Установка и запуск
  </strong>
</summary>

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/facirNew/code_redactor.git
   cd code_redactor
   ```

2. Создайте .env по образцу .env.example.

3. Соберите и запустите контейнер:
   ```bash
   docker-compose up --build
   ```

4. Запустите скрипт для заполнения базы тестовыми данными:
   ```bash
   python db_test_data.py
   ```

5. Используйте скрипт publisher.py для передачи сообщений в контейнер.

</details>
