import logging
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from install_sid import install_sid



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

args = {"owner": "ALEXANDREB", "start_date": datetime(2025, 1, 1)}

# Define the DAG
with DAG(
    dag_id="install_sid",
    default_args=args,
    schedule=None,
    catchup=False,
) as dag:
    def launch_install_sid():
        logger.info("Creating databases...")
        install_sid()
        logger.info("Databases created successfully.")

    install_sid_task = PythonOperator(task_id="install_sid", python_callable=launch_install_sid)