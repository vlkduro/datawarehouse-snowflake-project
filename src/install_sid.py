import os
from dotenv import load_dotenv
import snowflake.connector
from logger_setup import setup_logger

logger = setup_logger("install_sid.py")

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

# --- SQL directory path ---
sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db'))

def execute_sql_file(cursor, file_path):
    with open(file_path, 'r') as file:
        sql_statements = file.read()
        for statement in sql_statements.split(';'):
            if statement.strip():
                logger.info(f"Executing: {statement.strip()}...")
                try:
                    cursor.execute(statement)
                except Exception as e:
                    logger.error(f"Failed to execute statement: {statement.strip()}")
                    logger.exception(e)
                    raise

def main():
    ctx = snowflake.connector.connect(**conn_params)
    logger.info(f"Connecting to Snowflake as user: {conn_params['user']}...")
    cs = ctx.cursor()
    sql_file_order = ["init.sql", "script_creation_stg.sql", "script_creation_tch.sql", "script_creation_soc.sql"]
    
    try:
        for sql_file in sql_file_order:
            full_path = os.path.join(sql_dir, sql_file)
            logger.info(f"--- Executing file: {sql_file} ---")
            execute_sql_file(cs, full_path)
        logger.info("All SQL files executed successfully.")
    except Exception as e:
        logger.error("Error during SQL execution.")
    finally:
        cs.close()
        ctx.close()
        logger.info("Snowflake connection closed.")

# --- Run the script ---
if __name__ == '__main__':
    main()