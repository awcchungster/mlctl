from datetime import timedelta

from mlctl.airflow import DAG, step
from airflow.utils.dates import days_ago


input_data ='s3://mlctltest/example1_data/'

# import yaml
# with open('provider_local.yaml') as f:
#     provider = yaml.safe_load(f)


default_args = {
}
with DAG(
    dag_id='airflow-mlctl-example',
    default_args=default_args,
    description='A simple 3 step workflow',
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:

    # returns a S3 bucket with the processed data
    op1 = step.process(func_name='sk_learn.process', input=input_data, provider=provider)

    # # returns a model artifact
    # op2 = step.train(name='sk_learn.train', input=op1.output)

    # # creates endpoint, ends pipeline
    # op3 = step.deploy(name='sk_learn.deploy', input=op2.output)

    # op1 >> op2 >> op3