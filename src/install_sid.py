import os
from logger_setup import setup_logger
import utils

logger = setup_logger("install_sid.py")

# --- SQL directory path ---
sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db'))

def main():
    ctx = utils.connect_snowflake()
    cs = ctx.cursor()
    logger.info(f"Connecting to Snowflake as user: {utils.get_username()}...")
    sql_file_order = ["init.sql", "script_creation_stg.sql", "script_creation_tch.sql", "script_creation_soc.sql"]
    
    try:
        for sql_file in sql_file_order:
            full_path = os.path.join(sql_dir, sql_file)
            logger.info(f"--- Executing file: {sql_file} ---")
            utils.execute_sql_file(cs, full_path, logger)
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