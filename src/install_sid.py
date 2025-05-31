import os
from dotenv import load_dotenv
import snowflake.connector

# Load environment variables from ../.env
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)


# Snowflake connection parameters
conn_params = {
    'user': os.getenv("SNOWFLAKE_USER"),
    'password': os.getenv("SNOWFLAKE_PASSWORD"),
    'account': os.getenv("SNOWFLAKE_ACCOUNT"),  # like: xy12345.us-east-1
    'warehouse': os.getenv("SNOWFLAKE_WAREHOUSE"),
}

# Directory containing .sql files
sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db'))

def execute_sql_file(cursor, file_path):
    with open(file_path, 'r') as file:
        sql_statements = file.read()
        for statement in sql_statements.split(';'):
            if statement.strip():
                print(f"Executing: {statement.strip()}...")
                cursor.execute(statement)


def main():
    # Connect to Snowflake
    ctx = snowflake.connector.connect(**conn_params)
    cs = ctx.cursor()
    # Ensures all SQL files are executed in the correct order
    sql_file_order = ["init.sql", "script_creation_stg.sql", "script_creation_tch.sql", "script_creation_soc.sql"]
    try:
        for sql_file in sql_file_order:
            full_path = os.path.join(sql_dir, sql_file)
            print(f"\n--- Executing file: {sql_file} ---")
            execute_sql_file(cs, full_path)
    finally:
        cs.close()
        ctx.close()
        print("All SQL files executed successfully.")

# Run the script
if __name__ == '__main__':
    main()