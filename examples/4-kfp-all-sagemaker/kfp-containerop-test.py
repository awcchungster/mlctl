
import kfp
from kfp import dsl, onprem
import kfp.components as comp


@dsl.pipeline(
    name='mlctl_workflow',
    description='hello world')
def mlctl_pipeline(provider_yaml: str, data_input: str, training_hp: str):

    op1 = dsl.ContainerOp(name='Processing', 
        image='awcchungster/mlctl-kfp-component:latest',
        command='python /entrypoint.py',
        # arguments='-p \'{"mlctl_version":0.1,"infrastructure":[{"name":"awssagemaker","arn":"arn:aws:iam::436885317446:role/sm-execution","container_repo":"436885317446.dkr.ecr.us-east-1.amazonaws.com/mlctl-test"}],"resources":{"process":"ml.t3.medium","train":"ml.m5.large","deploy":"ml.t2.medium"},"metadata":[{"name":"mlflow","tracking_uri":"http://ec2-34-234-193-241.compute-1.amazonaws.com:5000"}]}\' --metadata \'{"project": "height_data", "job_type": "train"}\' --data \'{"input":"s3://mlctltest/example1_data/","output":"s3://mlctltest/example1_output/"}\''
    )

    # .apply(onprem.use_k8s_secret(secret_name='aws-secrets',
# k8s_secret_key_to_env={'secret_access': 'AWS_SECRET_ACCESS_KEY', 'access_key': 'AWS_ACCESS_KEY_ID'}))

    op2 = dsl.ContainerOp(name='Training', 
        image='awcchungster/mlctl-kfp-component:latest',
        command='python /entrypoint.py',
        # arguments='-p \'{"mlctl_version":0.1,"infrastructure":[{"name":"awssagemaker","arn":"arn:aws:iam::436885317446:role/sm-execution","container_repo":"436885317446.dkr.ecr.us-east-1.amazonaws.com/mlctl-test"}],"resources":{"process":"ml.t3.medium","train":"ml.m5.large","deploy":"ml.t2.medium"},"metadata":[{"name":"mlflow","tracking_uri":"http://ec2-34-234-193-241.compute-1.amazonaws.com:5000"}]}\' --metadata \'{"project": "height_data", "job_type": "process"}\' --data \'{"input":"s3://mlctltest/example1_data/","output":"s3://mlctltest/example1_output/"}\''
    )

    op2.after(op1)


kfp.compiler.Compiler().compile(mlctl_pipeline, 'mlctl_pipeline.yaml')

kfp.Client(host='http://localhost:8080').create_run_from_pipeline_package('mlctl_pipeline.yaml', arguments={})

# Scratch

# https://github.com/kubeflow/pipelines/blob/master/samples/core/pipeline_transformers/pipeline_transformers.py#L40
# dsl.get_pipeline_conf().add_op_transformer(add_annotation)