import logging

logging.basicConfig(
    filename='/opt/airflow/logs/error_log.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

logger = logging.getLogger(__name__)
