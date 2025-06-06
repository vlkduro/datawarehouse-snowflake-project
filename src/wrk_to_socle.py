from datetime import datetime
from logger_setup import setup_logger
import utils
import pandas as pd

logger = setup_logger("wrk_to_socle.py")
# Mapping des colonnes WRK ➝ SOCLE
column_mapping_chambre = {
    "NO_CHAMBRE": "ROOM_NUM",
    "NOM_CHAMBRE": "ROOM_NAME",
    "NO_ETAGE": "FLOOR_NUM",
    "NOM_BATIMENT": "BULD_NAME",
    "TYPE_CHAMBRE": "ROOM_TYP",
    "PRIX_JOUR": "ROOM_DAY_RATE",
    "DT_CREATION": "CRTN_DT",
    # EXEC_ID ajouté dynamiquement
}

column_mapping_medicament = {
    # "MEDC_ID" ajouté dynamiquement
    "CD_MEDICAMENT": "MEDC_CD",
    "NOM_MEDICAMENT": "MEDC_NAME",
    "CONDIT_MEDICAMENT": "MEDC_COND",
    "CATG_MEDICAMENT": "MEDC_CATG",
    "MAQUE_FABRI": "MANF_FABRI",
}

columns_mapping = {
    "CHAMBRE": column_mapping_chambre,
    "MEDICAMENT": column_mapping_medicament,
}


def retrieve_table_wrk(cnx, table_name):
    query = f"SELECT * FROM WRK.PUBLIC.{table_name}"
    df = pd.read_sql(query, cnx)
    return df


def map_and_prepare_data(table, table_name):
    # Appliquer le mapping
    mapped_table = table.rename(columns=column_mapping_chambre)

    # Ajout de EXEC_ID (timestamp d'exécution)
    exec_id = int(datetime.now().timestamp() / 1000)  # Convertir en millisecondes
    mapped_table["EXEC_ID"] = exec_id

    return mapped_table


def insert_data_in_socle(cs, table, table_name):
    cols = table.columns.tolist()
    col_names = ", ".join(cols)
    insert_query = (
        f"USE DATABASE SOC; "
        f"USE SCHEMA PUBLIC; "
        f"INSERT INTO R_ROOM ({col_names}) VALUES "
    )
    values = []
    for _, row in table.iterrows():
        row_values = []
        for value in row.tolist():
            if value is None:
                row_values.append("NULL")
            else:
                safe_value = str(value).replace("'", "''")
                row_values.append(f"'{safe_value}'")
        values.append(f"({', '.join(row_values)})")

    insert_query += ",\n".join(values) + ";"
    utils.execute_sql(cs, insert_query, logger)


def populate_socle_from_wrk():
    cnx = utils.connect_snowflake()
    cs = cnx.cursor()
    logger.info(
        f"Connecting to Snowflake for WRK ➝ SOCLE as user: {utils.get_username()}..."
    )

    table_name = "CHAMBRE"

    logger.info(f"Processing WRK ➝ SOCLE for table: {table_name}")

    table = retrieve_table_wrk(cnx, table_name)
    logger.info(f"Loaded data from WRK.{table_name} with {len(table)} rows")

    logger.info(f"Applying mapping and rules for SOCLE.{table_name}")
    mapped_table = map_and_prepare_data(table, table_name)

    logger.info(f"Inserting mapped data into SOC.R_ROOM")
    insert_data_in_socle(cs, mapped_table, table_name)

    cs.close()
    cnx.close()
    logger.info("Snowflake connection closed.")


"""_summary_
def main():
logger.info("Starting the population of SOCLE tables from WRK...")
populate_socle_from_wrk()
logger.info("SOCLE tables populated successfully.")


if __name__ == "__main__":
main()
"""
