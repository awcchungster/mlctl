from mlctl.airflow import DAG, step
import yaml

input_data ='s3://mlctltest/example1_data/'
# with open('provider_local.yaml') as f:
#     provider = yaml.safe_load(f)

with open('provider_mix.yaml') as f:
    provider = yaml.safe_load(f)

default_args = {
    provider=provider,
}
with DAG(
    'airflow-mlctl-example',
    default_args=default_args,
    description='A simple 3 step workflow',
    start_date=days_ago(2),
) as dag:

    # returns a S3 bucket with the processed data
    op1 = step.process(name='sk_learn.process', input=input_data, provider=provider)

    # # returns a model artifact
    # op2 = step.train(name='sk_learn.train', input=op1.output)

    # # creates endpoint, ends pipeline
    # op3 = step.deploy(name='sk_learn.deploy', input=op2.output)

    # op1 >> op2 >> op3