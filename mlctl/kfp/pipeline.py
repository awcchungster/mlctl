import kfp
from kfp import dsl

def run_pipeline(function, host):
    kfp.compiler.Compiler().compile(function, 'mlctl_pipeline.yaml')

    # change the host to where you want to submit the job
    kfp.Client(host=host).create_run_from_pipeline_package('mlctl_pipeline.yaml', arguments={})