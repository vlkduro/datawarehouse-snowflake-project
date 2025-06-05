from logger_setup import setup_logger
from install_sid import install_sid
from collect_stg_data import collect_stg_data
from launch_load_sid import launch_load_sid

from stg_to_wrk import populate_wrk_from_stg

logger = setup_logger("main.py")


def pipeline():
    logger.info("Starting the pipeline...")
    logger.info("Creating databases...")
    install_sid()
    logger.info("Databases created successfully.")
    logger.info("Starting data collection...")
    collect_stg_data()
    logger.info("Data collection completed successfully.")
    logger.info("Loading data into Snowflake...")
    launch_load_sid()
    logger.info("Data loaded successfully.")
    logger.info("Populating WRK tables from STG...")
    populate_wrk_from_stg()
    logger.info("WRK tables populated successfully.")


if __name__ == "__main__":
    pipeline()
