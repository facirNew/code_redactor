import asyncio
import os
import shutil
import subprocess

import conf
import loguru
import redis
from models import TaskData, TaskSolution
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

logger = loguru.logger
r = redis.Redis(host=conf.REDIS_HOST, port=conf.REDIS_PORT)
DATABASE_URL = (f'postgresql+asyncpg://{conf.POSTGRES_USER}:{conf.POSTGRES_PASSWORD}@'
                f'{conf.PGHOST}:{conf.PGPORT}/{conf.POSTGRES_DB}')
base = declarative_base()
engine = create_async_engine(DATABASE_URL)
pubsub = r.pubsub()
pubsub.psubscribe('channel_*')


async def fetch_data_from_db(solution_id: int) -> dict:
    code_data = {}
    testcases = {}
    async with engine.begin() as conn:
        code_data_cursor = await conn.execute(select(TaskSolution).where(TaskSolution.id == solution_id))
        for row in code_data_cursor:
            code_data = {'id': row.id, 'task': row.task, 'code': row.code}
        testcases_cursor = await conn.execute(select(TaskData).where(TaskData.task == code_data['task']))
        for testcase_row in testcases_cursor:
            testcases = {'id': testcase_row.id,
                         'task': testcase_row.task,
                         'input_data': testcase_row.input_data,
                         'output_data': testcase_row.output_data}
    return {'code_data': code_data, 'testcases': testcases}


async def insert_result(solution_id: int, data: dict) -> None:
    async with engine.begin() as conn:
        await conn.execute(update(TaskSolution).
                           where(TaskSolution.id == solution_id).
                           values(status=data['status'], output=data['output']))


async def run_code(ch: str, msg: str) -> None:
    code_data = await fetch_data_from_db(int(msg))
    logger.info(code_data)
    if not os.path.isdir(ch):
        os.makedirs(ch)
    with open(f'{ch}/code.py', 'w') as file:
        file.write(code_data['code_data']['code'])
    with open(f'{ch}/testcases.py', 'w') as file:
        file.write(f"case = {code_data['testcases']['input_data']}\n"
                   f"expected_result = {code_data['testcases']['output_data']}\n")
    shutil.copy('template/test_template.py', f'{ch}/test.py')
    result = subprocess.run(args=['python', 'test.py'],
                            capture_output=True,
                            cwd=f'./{ch}',
                            text=True,
                            check=False,
                            )
    logger.info('stdout: ' + result.stdout)
    logger.info('stderr: ' + result.stderr)
    data = {'status': 'complete', 'output': None}
    if result.stdout or result.stderr:
        data['status'] = 'error'
        data['output'] = result.stdout + result.stderr
    await insert_result(int(msg), data)
    shutil.rmtree(ch)


async def main():
    for message in pubsub.listen():
        if message.get('type', None) == 'pmessage':
            await run_code(ch=message.get('channel').decode('utf-8'),
                           msg=message.get('data').decode('utf-8'),
                           )
        else:
            logger.info(message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
