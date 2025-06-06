# collect_stg_data.py
import os
import csv
import re

from dotenv import load_dotenv
from logger_setup import setup_logger

logger = setup_logger("collect_stg_data.py")

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path)

base_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Data", "Data Hospital")
)
output_sql_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "db", "stg_data")
)
os.makedirs(output_sql_dir, exist_ok=True)


def extract_table_name(filename):
    return re.sub(r"[_]?\d{6,8}\.txt$", "", filename, flags=re.IGNORECASE).upper()


def generate_insert_sql_file(table_name, file_path, output_dir):
    sql_file_path = os.path.join(output_dir, f"insert_{table_name}.sql")
    with open(file_path, "r", encoding="utf-8") as f_in, open(
        sql_file_path, "a", encoding="utf-8"
    ) as f_out:
        f_out.write(f"USE DATABASE STG;\nUSE SCHEMA PUBLIC;\n\n")
        reader = csv.reader(f_in, delimiter=";")

        rows = list(reader)
        # Cas particulier, dans la table HOSPITALISATION, on enlève le suffixe _hospi des noms de colonnes
        col_names = [name.replace("_hospi", "") for name in rows[0] if name != ""]
        rows = rows[1:]

        if not rows:
            logger.warning(f"[SKIP] {file_path} is empty.")
            return

        logger.info(
            f"Generating SQL file {sql_file_path} with {len(rows)} rows for table {table_name}"
        )

        values_list = []

        for row in rows:
            row.pop(0)  # Remove the first column as it is unused
            escaped_values = ["'" + str(val).replace("'", "''") + "'" for val in row]
            values_list.append(f"({', '.join(escaped_values)})")

        # Une seule requête INSERT
        sql = (
            f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES\n"
            + ",\n".join(values_list)
            + ";\n"
        )
        f_out.write(sql)


def collect_stg_data():
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path) and folder.startswith("BDD_HOSPITAL_"):
            logger.info(f"Processing folder: {folder}")
            for file in os.listdir(folder_path):
                if file.endswith(".txt"):
                    file_path = os.path.join(folder_path, file)
                    table_name = extract_table_name(file)
                    logger.info(
                        f"Generating SQL from file: {file} into table: {table_name}"
                    )
                    generate_insert_sql_file(table_name, file_path, output_sql_dir)
