# execute_stg_sql.py
import os
from logger_setup import setup_logger
import utils

logger = setup_logger("launch_load_sid.py")

sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'stg_data'))

def main():
    logger.info("Connecting to Snowflake...")
    ctx = utils.connect_snowflake()
    cs = ctx.cursor()
    try:
        utils.execute_sql_file(cs, sql_dir, logger)
    finally:
        cs.close()
        ctx.close()
        logger.info("Snowflake connection closed.")

if __name__ == '__main__':
    main()
