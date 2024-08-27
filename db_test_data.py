import asyncio

from asyncpg_lite import DatabaseManager
from sqlalchemy import JSON, Integer, String, Text


async def main() -> None:
    """
    Создание таблиц и заполнение базы тестовыми данными
    """

    db_manager = DatabaseManager(auth_params={'host': 'localhost',
                                              'port': 5434,
                                              'user': 'postgres',
                                              'password': 'postgres',
                                              'database': 'interpreter_test'},
                                 deletion_password='postgres',
                                 )

    async with db_manager as manager:
        task_columns = [
            {'name': 'id', 'type': Integer, 'options': {
                'primary_key': True,
                'autoincrement': True,
                'unique': True},
             },
            {'name': 'tag', 'type': String},
            {'name': 'body', 'type': Text},
        ]
        task_data_columns = [
            {'name': 'id', 'type': Integer, 'options': {
             'primary_key': True,
             'autoincrement': True,
             'unique': True},
             },
            {'name': 'task', 'type': Integer},
            {'name': 'input_data', 'type': JSON},
            {'name': 'output_data', 'type': JSON},
        ]
        task_solution_columns = [
            {'name': 'id', 'type': Integer, 'options': {
             'primary_key': True,
             'autoincrement': True,
             'unique': True},
             },
            {'name': 'task', 'type': Integer},
            {'name': 'code', 'type': Text},
            {'name': 'status', 'type': String},
            {'name': 'output', 'type': Text, 'options': {'nullable': True}},
        ]

        await manager.create_table(table_name='task', columns=task_columns)
        await manager.create_table(table_name='task_data', columns=task_data_columns)
        await manager.create_table(table_name='task_solution', columns=task_solution_columns)

        task = [
            {'id': 1, 'tag': 'algorythm', 'body': 'Напишите функцию для суммирования двух чисел'},
            {'id': 2, 'tag': 'algorythm', 'body': 'Напишите функцию для деления двух чисел'},
        ]
        task_data = [
            {'id': 1, 'task': 1, 'input_data': ['1, 2', '0, 0', '3, -5'], 'output_data': [3, 0, -2]},
            {'id': 2, 'task': 2, 'input_data': ['1, 2', '3, 1', '4, 2'], 'output_data': [0.5, 3.0, 2.0]},
        ]
        solutions = [
            {'id': 1, 'task': 1, 'code': 'def summary(x, y):\n'
                                         '    print(x + y)\n\n'
                                         'x = int(input())\n'
                                         'y = int(input())\n'
                                         'summary(x, y)\n',
             'status': 'in_progress\n'},
            {'id': 2, 'task': 2, 'code': 'def devision(x, y):\n'
                                         '    print(x / y)\n\n'
                                         'x = int(input())\n'
                                         'y = int(input())\n'
                                         'devision(x, y)\n',
             'status': 'in_progress'},
            {'id': 3, 'task': 2, 'code': 'def devision(x, y):\n'
                                         '    print(x  y)\n\n'
                                         'x = int(input())\n'
                                         'y = int(input())\n'
                                         'devision(x, y)\n',
             'status': 'in_progress'},
            {'id': 4, 'task': 1, 'code': 'from time import sleep\n\n'
                                         'def devision(x, y):\n'
                                         '    sleep(10)\n'
                                         '    print(x / y)\n\n'
                                         'x = int(input())\n'
                                         'y = int(input())\n'
                                         'devision(x, y)\n',
             'status': 'in_progress'},
            {'id': 5, 'task': 1, 'code': 'def devision(x, y):\n'
                                         '    print(x - y)\n\n'
                                         'x = int(input())\n'
                                         'y = int(input())\n'
                                         'devision(x, y)\n',
             'status': 'in_progress'},
        ]
        await manager.insert_data_with_update(table_name='task', records_data=task, conflict_column='id')
        await manager.insert_data_with_update(table_name='task_data', records_data=task_data, conflict_column='id')
        await manager.insert_data_with_update(table_name='task_solution', records_data=solutions, conflict_column='id')


if __name__ == '__main__':
    asyncio.run(main())
