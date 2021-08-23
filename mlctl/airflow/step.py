from airflow.operators.python import PythonOperator

def process(func_name, input, provider):

    def process_job(job_spec, provider_spec):
        job = parse_process_specs(job_spec, provider_spec)
        process = determine_infra_plugin_from_job(job)
        result = process.start_process(job)

        
        print(result)

    job_spec = {
        "mlctl_version": 0.1,
        "metadata": {
            "version": 1,
            "project": "weight_data_aws",
            "job_type": "process"
        },
        "data": {
            "input": "s3://mlctltest/example1_data/",
            "output": "s3://mlctltest/example1_data_out/"
        }
    }

    return PythonOperator(
        task_id='mlctl_process',
        python_callable=process_job,
        op_kwargs={
            'job_spec': job_spec,
            'provider_spec': provider},
    )

def train():
    pass

def deploy():
    pass