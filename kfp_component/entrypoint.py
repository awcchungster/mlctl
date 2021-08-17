import argparse
import sys
import yaml
import json
import pprint
from pathlib import Path

sys.path.insert(0, '..')

from mlctl.clis.common.utils import determine_infra_plugin_from_job, parse_train_yamls, parse_process_yamls, parse_deploy_yamls, docker_instructions

import sys
print(sys.argv)

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output")
parser.add_argument("-p", "--provider")
parser.add_argument("-t", "--task")
parser.add_argument("--metadata")
parser.add_argument("--envvars")
parser.add_argument("--data")
parser.add_argument("--models")
args = parser.parse_args()

# convert provider.yaml to file
if args.provider:
    provider = json.loads(args.provider)
    with open('./provider.yaml', 'w') as outfile:
        yaml.dump(provider, outfile, default_flow_style=False)

# convert job.yaml to file
job_yaml = {}

if args.metadata:
    job_yaml['metadata'] = json.loads(args.metadata)

if args.envvars:
    job_yaml['env_vars'] = json.loads(args.envvars)

if args.data:
    job_yaml['data'] = json.loads(args.data)

if args.models:
    job_yaml['models'] = json.loads(args.models)

# figure what task this is
if args.task:
    task = args.task
elif 'job_type' in job_yaml['metadata']:
    task = job_yaml['metadata']['job_type']

print('Processed YAML:')
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(job_yaml)

# for key, value in metadata.items():
#     job_yaml['metadata'][key] = value

# for key, value in envvars.items():
#     job_yaml['env_vars'][key] = value

# for key, value in data.items():
#     job_yaml['data'][key] = value

if task == 'process':
    with open('./process.yaml', 'w') as outfile:
        yaml.dump(job_yaml, outfile, default_flow_style=False)

    job = parse_process_yamls('./process.yaml', './provider.yaml')
    process = determine_infra_plugin_from_job(job)
    process_run = process.start_process(
        job)
    pp.pprint(process_run)

    process.get_process_info(job, loop=True)

elif task == 'train':
    with open('./train.yaml', 'w') as outfile:
        yaml.dump(job_yaml, outfile, default_flow_style=False)

    job = parse_train_yamls('./train.yaml', './provider.yaml')
    # pp.pprint(job.serialize())
    train = determine_infra_plugin_from_job(job)

    train_run = train.start_train(job)
    print('Infra Job Spec:')
    pp.pprint(train_run)
    
    train.get_train_info(job, loop=True)

elif task == 'deploy':
    with open('./deploy.yaml', 'w') as outfile:
        yaml.dump(job_yaml, outfile, default_flow_style=False)

    job = parse_deploy_yamls('./deploy.yaml', './provider.yaml')
    deploy = determine_infra_plugin_from_job(job)

    deploy.create(job)
    deploy_run = deploy.start_deploy(job)
    print('Infra Job Spec:')
    pp.pprint(deploy_run)
    
    deploy.get_deploy_info(job, loop=True)

else:
    print("Unknown Task")

# TODO: do not run when in testing mode
Path("/opt/ml/").mkdir(parents=True, exist_ok=True)
with open("/opt/ml/outputs", "w") as outfile:
    json.dump({"success": True}, outfile)

job_type = job.serialize()['job_type']
infrastructure = job.serialize()['infrastructure'][job_type]['name']
resources = job.serialize()['infrastructure'][job_type]['resources']
metadata = {
   "outputs":[
      {
         "storage":"inline",
         "source":f"## Infrastructure\n### {infrastructure} \n## Resources\n### {resources}\n## Est. Cost\n### $0.15",
         "type":"markdown"
      }
   ]
}

with open('/mlpipeline-ui-metadata.json', 'w') as metadata_file:
    json.dump(metadata, metadata_file)


# Processing
# python3 entrypoint.py -p '{"mlctl_version":0.1,"infrastructure":[{"name":"awssagemaker","arn":"arn:aws:iam::436885317446:role/sm-execution","container_repo":"436885317446.dkr.ecr.us-east-1.amazonaws.com/mlctl-test"}],"resources":{"process":"ml.t3.medium","train":"ml.m5.large","deploy":"ml.t2.medium"},"metadata":[{"name":"mlflow","tracking_uri":"http://ec2-34-234-193-241.compute-1.amazonaws.com:5000"}]}' --metadata '{"project": "height_data", "job_type": "process"}' --data '{"input":"s3://mlctltest/example1_data/","output":"s3://mlctltest/example1_output/"}'

# Training Job
# python3 entrypoint.py -p '{"mlctl_version":0.1,"infrastructure":[{"name":"awssagemaker","arn":"arn:aws:iam::436885317446:role/sm-execution","container_repo":"436885317446.dkr.ecr.us-east-1.amazonaws.com/mlctl-test"}],"resources":{"process":"ml.t3.medium","train":"ml.m5.large","deploy":"ml.t2.medium"},"metadata":[{"name":"mlflow","tracking_uri":"http://ec2-34-234-193-241.compute-1.amazonaws.com:5000"}]}' --data '{"input":"s3://mlctltest/example1_data/","output":"s3://mlctltest/example1_output/"}' --envvars '{"hp_eta":0.3,"hp_max_depth":3,"hp_objective":"multi:softprob","hp_num_class":3}' --metadata '{"project": "height_data", "job_type": "train"}'
