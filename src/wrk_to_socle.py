from logger_setup import setup_logger
import utils
import os

logger = setup_logger("wrk_to_socle.py")

def populate_socle_from_wrk() -> None:
    with utils.connect_snowflake() as conn:  
        cs = conn.cursor()
        sql_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db'))
        full_path = os.path.join(sql_dir, "wrk_to_soc.sql")
        utils.execute_sql_file(cs, full_path, logger)