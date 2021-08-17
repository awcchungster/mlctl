from kfp import onprem, dsl
import kfp.components as comp
from kubernetes.client.models import V1EnvVar
import yaml
import json
# def process(provider, name=None, env_vars=None, input=None):

#     provider 

#     data_string = '\'{input: "{inputValue: data}", output: "{outputValue}"}\''

#     component_json = {
#         'name': name,
#         'description': 'mlctl Process Job',
#         'inputs': [
#             f"{{name: metadata, type: Dict}}",
#             f"{{name: data, type: Dict}}",
#             f"{{name: provider, type: Dict}}",
#         ], 'outputs': [
#             f"{{name: data}}",
#         ], 'implementation': {
#             'container': {
#                 'image': 'awcchungster/mlctl-kfp-component:latest',
#                 'command': 'python entrypoint.py -p {inputValue: provider} --metadata {inputValue: metadata} --data {inputValue: data}'
#             }
#         }
#     }
#     # define the component
#     # convert component to Op
#     with open('./mlctl_kfp_process.yaml', 'w') as outfile:
#         yaml.dump(component_json, outfile, default_flow_style=False)

#     # add specifics
#     data = {"input":input,"output":"s3://mlctltest/example1_filtered/"}

#     metadata={"project": "height_data", "job_type": "process"}

#     yaml_text = yaml.dump(component_json)
#     print(yaml_text)
#     temp_component = comp.load_component_from_text(yaml_text)

    # temp_component = comp.load_component_from_text(component_json)

#     temp_component = comp.load_component_from_text("""
# name: Get Lines
# description: Gets the specified number of lines from the input file.

# inputs:
# - {name: metadata, type: Dict, description: 'Data for input 1'}
# - {name: provider, type: Dict, description: 'Data for input 1'}
# - {name: data, type: Dict, default: '100', description: 'Number of lines to copy'}

# outputs:
# - {name: data, type: String, description: 'Output 1 data.'}

# implementation:
#   container:
#     image: gcr.io/my-org/my-image@sha256:a172..752f
#     # command is a list of strings (command-line arguments). 
#     # The YAML language has two syntaxes for lists and you can use either of them. 
#     # Here we use the "flow syntax" - comma-separated strings inside square brackets.
#     command: [
#       python3, 
#       # Path of the program inside the container
#       /pipelines/component/src/program.py,
#       --input1-path,
#       {inputValue: metadata},
#       --param1, 
#       {inputValue: data},

#       {inputValue: provider},
#       --output1-path, 
#       {outputPath: data},
#     ]""")

    
    
    # op1 = temp_component(metadata=metadata, data=data, provider=provider)
    # op1.add_env_variable(V1EnvVar(name='AWS_DEFAULT_REGION', value='us-east-1'))
    # op1.apply(onprem.use_k8s_secret(secret_name='aws-secrets', k8s_secret_key_to_env={'secret_access': 'AWS_SECRET_ACCESS_KEY', 'access_key': 'AWS_ACCESS_KEY_ID'}))
    # op1.execution_options.caching_strategy.max_cache_staleness = "P0D"
    # return op1

def process(provider, name=None, env_vars=None, input=None):
    # print(input)

    provider = json.dumps(provider)
    data = json.dumps({"input":input,"output":"s3://mlctltest/example1_filtered/"})

    metadata=json.dumps({"project": "height_data", "job_type": "process"})
    op1 = dsl.ContainerOp(name='Process', 
        image='awcchungster/mlctl-kfp-component:latest',
        command='/bin/sh',
        arguments=['-c', f"python entrypoint.py -o 'opt/ml/processing/outputs' -p '{provider}' --metadata '{metadata}' --data '{data}'"],
        file_outputs={
            'data': '/opt/ml/outputs',
            'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'
        }
    )
    
    op1.add_env_variable(V1EnvVar(name='AWS_DEFAULT_REGION', value='us-east-1'))
    op1.apply(onprem.use_k8s_secret(secret_name='aws-secrets', k8s_secret_key_to_env={'secret_access': 'AWS_SECRET_ACCESS_KEY', 'access_key': 'AWS_ACCESS_KEY_ID'}))
    op1.execution_options.caching_strategy.max_cache_staleness = "P0D"
    return op1

def train(provider, name=None, env_vars=None, input=None):
    provider = json.dumps(provider)
    data = json.dumps({"input":"s3://mlctltest/example1_filtered/","output":"s3://mlctltest/example1_output/"})
    metadata= json.dumps({"project": "height_data", "job_type": "train"})
    op2 = dsl.ContainerOp(name='Train', 
        image='awcchungster/mlctl-kfp-component:latest',
        command='/bin/sh',
        arguments=['-c', f"python entrypoint.py -p '{provider}' --metadata '{metadata}' --data '{data}'"],
        file_outputs={
            'model-artifact': '/opt/ml/outputs',
            'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'
        }
    )
    
    op2.add_env_variable(V1EnvVar(name='AWS_DEFAULT_REGION', value='us-east-1'))
    op2.apply(onprem.use_k8s_secret(secret_name='aws-secrets', k8s_secret_key_to_env={'secret_access': 'AWS_SECRET_ACCESS_KEY', 'access_key': 'AWS_ACCESS_KEY_ID'}))
    op2.execution_options.caching_strategy.max_cache_staleness = "P0D"
    return op2

def train(provider, name=None, env_vars=None, input=None):
    provider = json.dumps(provider)
    data = json.dumps({"input":"s3://mlctltest/example1_filtered/","output":"s3://mlctltest/example1_output/"})
    metadata= json.dumps({"project": "height_data", "job_type": "train"})
    op2 = dsl.ContainerOp(name='Train', 
        image='awcchungster/mlctl-kfp-component:latest',
        command='/bin/sh',
        arguments=['-c', f"python entrypoint.py -p '{provider}' --metadata '{metadata}' --data '{data}'"],
        file_outputs={
            'model-artifact': '/opt/ml/outputs',
            'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'
        }
    )
    
    op2.add_env_variable(V1EnvVar(name='AWS_DEFAULT_REGION', value='us-east-1'))
    op2.apply(onprem.use_k8s_secret(secret_name='aws-secrets', k8s_secret_key_to_env={'secret_access': 'AWS_SECRET_ACCESS_KEY', 'access_key': 'AWS_ACCESS_KEY_ID'}))
    op2.execution_options.caching_strategy.max_cache_staleness = "P0D"
    return op2

def deploy(provider, name=None, input=None): 
    provider = json.dumps(provider)
    model = json.dumps({"artifact":"s3://mlctltest/example1_output/mlctl-stumblebum-lenitives/output/model.tar.gz"})
    metadata=json.dumps({"project": "height_data", "job_type": "deploy"})

    # metadata={"project": "height_data", "job_type": "train"}
    # 'python entrypoint.py -p \'{"mlctl_version":0.1,"infrastructure":[{"name":"awssagemaker","arn":"arn:aws:iam::436885317446:role/sm-execution","container_repo":"436885317446.dkr.ecr.us-east-1.amazonaws.com/mlctl-test"}],"resources":{"process":"ml.t3.medium","train":"ml.m5.large","deploy":"ml.t2.medium"} }\' --metadata \'{"project": "height_data", "job_type": "deploy"}\' --model \'{"artifact":"s3://mlctltest/example1_output/mlctl-stumblebum-lenitives/output/model.tar.gz"}\''

    op3 = dsl.ContainerOp(name='Deploy', 
        image='awcchungster/mlctl-kfp-component:latest',
        command='/bin/sh',
        arguments=['-c', f"python entrypoint.py -p '{provider}' --metadata '{metadata}' --model '{model}'"],
        file_outputs={
            'data': '/opt/ml/outputs',
            'mlpipeline-ui-metadata': '/mlpipeline-ui-metadata.json'
        }
    )
    
    op3.add_env_variable(V1EnvVar(name='AWS_DEFAULT_REGION', value='us-east-1'))
    op3.apply(onprem.use_k8s_secret(secret_name='aws-secrets', k8s_secret_key_to_env={'secret_access': 'AWS_SECRET_ACCESS_KEY', 'access_key': 'AWS_ACCESS_KEY_ID'}))
    op3.execution_options.caching_strategy.max_cache_staleness = "P0D"
    return op3
