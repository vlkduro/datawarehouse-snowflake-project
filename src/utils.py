from datetime import datetime
import os
from dotenv import load_dotenv
import snowflake.connector
from logger_setup import setup_logger

# --- Load environment variables ---
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)

# --- Snowflake connection parameters ---
conn_params = {
    'user': os.getenv("SNOWFLAKE_USER"),
    'password': os.getenv("SNOWFLAKE_PASSWORD"),
    'account': os.getenv("SNOWFLAKE_ACCOUNT"),  # like: xy12345.us-east-1
    'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
}

def connect_snowflake():
    ctx = snowflake.connector.connect(**conn_params)
    return  ctx

def get_username():
    return conn_params.get('user', 'unknown_user')

def execute_sql_file(cursor, file_path, logger):
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_statements = file.read()
        for statement in sql_statements.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception as e:
                    logger.error(f"Failed to execute statement: {statement.strip()}")
                    logger.exception(e)
                    raise