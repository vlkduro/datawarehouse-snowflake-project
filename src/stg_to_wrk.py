from datetime import datetime
from logger_setup import setup_logger
import utils
import pandas as pd

logger = setup_logger("stg_to_wrk.py")


def str_to_timezone(timezone_str):
    parts = timezone_str.split("-")
    # Special case where the data is completely missing
    if len(parts) == 1 and ("00" in parts or "NULL" in parts):
        parts = "0001-01-01-00-00-00".split("-")
    # Data is missing, we retreive the most out of the correct data
    if "##" in parts:
        missing_data = False
        for i, part in enumerate(parts):
            if part == "##":
                missing_data = True
            if missing_data:
                parts[i] = "00"
    # Only Year-Month-Day is provided
    if len(parts) == 3:
        parts += ["00", "00", "00"]
    timezone_str = "-".join(parts)
    timezone = datetime.strptime(timezone_str, "%Y-%m-%d-%H-%M-%S")
    return timezone


ruleset = {
    "MEDICAMENT": {},
    "PATIENT": {
        "TS_CREATION_PATIENT": str_to_timezone,
        "TS_MAJ_PATIENT": str_to_timezone,
    },
    "TRAITEMENT": {
        "TS_CREATION_TRAITEMENT": str_to_timezone,
    },
    "PERSONNEL": {
        "TS_DEBUT_ACTIVITE": str_to_timezone,
        "TS_FIN_ACTIVITE": str_to_timezone,
        "TS_CREATION_PERSONNEL": str_to_timezone,
        "TS_MAJ_PERSONNEL": str_to_timezone,
    },
    "CONSULTATION": {
        "TS_DEBUT_CONSULT": str_to_timezone,
        "TS_FIN_CONSULT": str_to_timezone,
    },
    "CHAMBRE": {},
    "HOSPITALISATION": {
        "TS_DEBUT_HOSPI": str_to_timezone,
        "TS_FIN_HOSPI": str_to_timezone,
    },
}

# Returns a dataframe
def retreive_table(cnx, table_name):
    query = f"SELECT * FROM STG.PUBLIC.{table_name}"
    df = pd.read_sql(query, cnx)
    return df


def sanitize_data(table, table_name):
    rules = ruleset.get(table_name)
    cols = table.columns.tolist()
    for col in cols:
        # For each column, we apply the corresponding function if it exists
        if col in rules:
            logger.info(f"Sanitizing column: {table_name}.{col}")
            func = rules[col]
            table[col] = table[col].apply(func)

def insert_data_in_wrk(cs, table, table_name):
    # Insert data into the WRK table
    cols = table.columns.tolist()
    col_names = ', '.join(cols)
    insert_query = (f'USE DATABASE WRK; '
                    f'USE SCHEMA PUBLIC; '
                    f'INSERT INTO {table_name} ({col_names}) VALUES')
    values = []
    for _, row in table.iterrows():
        values.append(f"({', '.join(
            [f"'{str(value)}'" for value in row.tolist()]
        )})")

    insert_query += ",\n".join(values) + ";"
    utils.execute_sql(cs, insert_query, logger)

def populate_wrk_from_stg():
    cnx = utils.connect_snowflake()
    cs = cnx.cursor()
    logger.info(f"Connecting to Snowflake as user: {utils.get_username()}...")
    # Important for constraints
    table_order = [
        "MEDICAMENT", "PATIENT", "TRAITEMENT", "PERSONNEL", "CONSULTATION", "CHAMBRE", "HOSPITALISATION"
    ]
    for table_name in table_order:
        logger.info(f"Processing table: {table_name}")
        # try:
        # Is a pandas dataframe
        table = retreive_table(cnx, table_name)
        logger.info(f"Loaded data from STG.{table_name} with {len(table)} rows")
        # Sanitize data if needed
        logger.info(f"Sanitizing data for {table_name}")
        sanitize_data(table, table_name)
        # Insert data from staging to working table
        logger.info(f"Data inserting into WRK.{table_name} successfully.")
        insert_data_in_wrk(cs, table, table_name)
        # except Exception as e:
        #     logger.error(f"Error processing table {table_name}: {e}")
    cs.close()
    cnx.close()
    logger.info("Snowflake connection closed.")
