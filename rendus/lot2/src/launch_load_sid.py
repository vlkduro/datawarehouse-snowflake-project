# execute_stg_sql.py
import os
from logger_setup import setup_logger
import utils

logger = setup_logger("launch_load_sid.py")

sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'stg_data'))

def launch_load_sid():
    logger.info("Connecting to Snowflake...")
    ctx = utils.connect_snowflake()
    cs = ctx.cursor()
    try:
        sql_files = [sql_file for sql_file in os.listdir(sql_dir) if sql_file.endswith('.sql')]
        for sql_file in sql_files:
            full_path = os.path.join(sql_dir, sql_file)
            logger.info(f"--- Executing file: {sql_file} ---")
            utils.execute_sql_file(cs, full_path, logger)
    finally:
        cs.close()
        ctx.close()
        logger.info("Snowflake connection closed.")


