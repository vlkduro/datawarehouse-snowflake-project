import logging
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from collect_stg_data import collect_stg_data
from launch_load_sid import launch_load_sid
from wrk_to_socle import populate_socle_from_wrk
from stg_to_wrk import populate_wrk_from_stg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

args = {"owner": "ALEXANDREB", "start_date": datetime(2025, 1, 1)}

# Define the DAG
with DAG(
    dag_id="load_sid",
    default_args=args,
    schedule=None,
    catchup=False,
) as dag:
    def launch_collect_stg_data():
        logger.info("Starting data collection...")
        collect_stg_data()
        logger.info("Data collection completed successfully.")

    def start_load_sid():
        logger.info("Loading data into Snowflake...")
        launch_load_sid()
        logger.info("Data loaded successfully.")

    def launch_populate_wrk_from_stg():
        logger.info("Populating WRK tables from STG...")
        populate_wrk_from_stg()
        logger.info("WRK tables populated successfully.")

    def launch_populate_socle_from_wrk():
        logger.info("Populating SOC tables from WRK...")
        populate_socle_from_wrk()
        logger.info("SOC tables populated successfully.")

    collect_stg_task = PythonOperator(task_id="collect_stg_data", python_callable=launch_collect_stg_data)
    load_sid_task = PythonOperator(task_id="populate_stg", python_callable=start_load_sid)
    populate_wrk_from_stg_task = PythonOperator(task_id="populate_wrk_from_stg", python_callable=launch_populate_wrk_from_stg)
    populate_socle_from_wrk_task = PythonOperator(task_id="populate_socle_from_wrk", python_callable=launch_populate_socle_from_wrk)

    collect_stg_task >> load_sid_task >> populate_wrk_from_stg_task >> populate_socle_from_wrk_task