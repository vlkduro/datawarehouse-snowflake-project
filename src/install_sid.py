import sqlite3
import os

sql_init_script_path = "db/init.sql"
sql_script_path = "db/script_creation_stg.sql"
db_path = "db/stg/stg_database.db"

# Création d'un directory pour la base de données si elle n'existe pas
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))
    print(f"Created directory for database: {os.path.dirname(db_path)}")
    print(f"Using database path: {db_path}")
else:
    print(f"Database directory already exists: {os.path.dirname(db_path)}")
    print(f"Using existing database path: {db_path}")


# SQLITE3
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if os.path.exists(sql_init_script_path):
        print(f"Skipping {sql_init_script_path} (not applicable for SQLite)")

    # Execution du init. Creation de la base de données
    print(
        f"Execution SQL Init script: {sql_init_script_path} (not applicable for SQLite)"
    )
    with open(sql_init_script_path, "r") as file:
        sql_init_script = file.read()
    cursor.executescript(sql_init_script)
    print("SQL Init script executed successfully.")
    print(f"Executing SQL script: {sql_script_path}")

    # Création de la base de données STG
    with open(sql_script_path, "r") as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
    print("STG database created successfully.")

except sqlite3.Error as e:
    print(f"An error occurred while creating the STG database: {e}")
finally:
    if "conn" in locals():
        conn.commit()
        cursor.close()
        conn.close()
        print("Database connection closed.")
