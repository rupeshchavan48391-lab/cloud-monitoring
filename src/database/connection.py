import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


DATABASE_CONFIG = {
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": os.getenv("DATABASE_PORT", "5432"),
    "dbname": os.getenv("DATABASE_NAME", "cloudmon"),
    "user": os.getenv("DATABASE_USER", "cloudmon_user"),
    "password": os.getenv("DATABASE_PASSWORD"),
}


def get_connection():
    return psycopg.connect(**DATABASE_CONFIG)
