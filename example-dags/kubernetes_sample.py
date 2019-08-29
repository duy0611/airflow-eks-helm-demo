import airflow
from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kubernetes_sample', 
    default_args=default_args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60))


start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(
    namespace='default',
    image="python:3.6",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="passing-test",
    task_id="passing-task",
    get_logs=True,
    in_cluster=True,
    is_delete_operator_pod=True,
    dag=dag
)

failing = KubernetesPodOperator(
    namespace='default',
    image="ubuntu:16.04",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="fail",
    task_id="failing-task",
    get_logs=True,
    in_cluster=True,
    is_delete_operator_pod=True,
    dag=dag
)

another_passing = KubernetesPodOperator(
        namespace='default',
        image="ubuntu:16.04",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        name="another-passing",
        task_id="another-passing",
        get_logs=True,
        in_cluster=True,
        is_delete_operator_pod=True,
        dag=dag
)

passing.set_upstream(start)
failing.set_upstream(start)
another_passing.set_upstream(start)
