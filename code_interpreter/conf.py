import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGDATA = os.getenv('PGDATA')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
