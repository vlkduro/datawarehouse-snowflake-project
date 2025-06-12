
from logger_setup import setup_logger
import utils
import pandas as pd
import os

logger = setup_logger("socle_to_csv.py")

# Returns a dataframe
def retreive_table(cnx, table_name):
    query = f"SELECT * FROM SOC.PUBLIC.{table_name}"
    df = pd.read_sql(query, cnx)
    return df

def generate_csv_from_socle():
    logger.info("Connecting to Snowflake...")
    with utils.connect_snowflake() as conn:
        cs = conn.cursor()
        try:
            tables = ["o_addr", "o_cons", "o_hosp", "o_indv", "o_stff", "o_telp", "o_tret", "r_medc", "r_part", "r_room"]
            for table_name in tables:
                try:
                    logger.info(f"Retrieving data from {table_name} table...")
                    df = retreive_table(conn, table_name)
                    csv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'socle-csv'))
                    if not os.path.exists(csv_dir):
                        os.makedirs(csv_dir)
                        logger.info(f"Created directory: {csv_dir}")
                    csv_file_path = os.path.join(csv_dir, f"soc.public.{table_name}.csv")
                    df.to_csv(csv_file_path, index=False)
                    logger.info(f"Data from {table_name} table saved to {csv_file_path}")
                except Exception as e:
                    logger.error(f"Error retrieving or saving data from {table_name} table: {e}")
        finally:
            cs.close()
            logger.info("Snowflake connection closed.")