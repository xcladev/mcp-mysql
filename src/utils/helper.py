import pymysql
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

@contextmanager
def get_db_connection():
    """Context manager for handling database connections using pymysql."""
    connection = None
    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset='utf8mb4',
            autocommit=True
        )
        yield connection
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")
    finally:
        if connection:
            connection.close()