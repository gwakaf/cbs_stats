from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}
start_date=datetime(2024, 1, 1)


with DAG(
    dag_id="reddit_pipeline_dag",
    description="Reddit ELT",
    schedule_interval="0 0 * * 1",  # Runs every Monday at midnight
    default_args=default_args,
    start_date=start_date,
    catchup=False,
    max_active_runs=1,
    tags=["RedditETL"],
) as dag:
    
    run_tests = BashOperator(
        task_id="run_tests",
        bash_command="pytest /opt/airflow/test/test_reddit_etl.py --maxfail=1 -v",
        dag=dag
    )

    extract_reddit_data = BashOperator(
        task_id="extract_reddit_data",
        bash_command="python /opt/airflow/src/reddit_stats.py {{ ds_nodash }}",
        dag=dag,
    )

    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command="python /opt/airflow/src/upload_to_s3.py {{ ds_nodash }}",
        dag=dag,
    )
    
    copy_to_redshift = BashOperator(
        task_id="copy_to_redshift",
        bash_command=f"python /opt/airflow/src/redshift.py {{ ds_nodash }}",
        dag=dag,
    )
    
run_tests >> extract_reddit_data >> upload_to_s3 >> copy_to_redshift

