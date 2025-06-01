# execute_stg_sql.py
import os
import snowflake.connector
from dotenv import load_dotenv
from logger_setup import setup_logger

logger = setup_logger("launch_load_sid.py")

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)

conn_params = {
    'user': os.getenv("SNOWFLAKE_USER"),
    'password': os.getenv("SNOWFLAKE_PASSWORD"),
    'account': os.getenv("SNOWFLAKE_ACCOUNT"),
    'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
    'database': 'STG',
    'schema': 'PUBLIC'
}

sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'stg_data'))

def execute_sql_files(cursor, sql_dir):
    sql_files = sorted([f for f in os.listdir(sql_dir) if f.endswith('.sql')])
    for file in sql_files:
        file_path = os.path.join(sql_dir, file)
        logger.info(f"Executing SQL file: {file}")
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            for statement in sql_script.strip().split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        logger.error(f"Error in {file}: {e}\nStatement: {statement}")
        logger.info(f"Finished executing {file}")

def main():
    logger.info("Connecting to Snowflake...")
    ctx = snowflake.connector.connect(**conn_params)
    cs = ctx.cursor()
    try:
        execute_sql_files(cs, sql_dir)
    finally:
        cs.close()
        ctx.close()
        logger.info("Snowflake connection closed.")

if __name__ == '__main__':
    main()
