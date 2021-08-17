# Set up the Component Container

In the parent mlctl directory, run the following command so the local context picks up the entire package.

`docker build -f ./kfp_component/Dockerfile .  -t mlctl-kfp`
`docker tag mlctl-kfp awcchungster/mlctl-kfp-component:latest`
`docker push awcchungster/mlctl-kfp-component:latest`

# Example Usage

This container reads command arguments in the entrypoint to dictate what it should run and deploy. 

- p = provider YAML in JSON form
- data = data section of the job YAML in JSON
- metadata = metadata section of the job YAML in JSON

Example:
```
python3 entrypoint.py -p '{"mlctl_version":0.1,"infrastructure":[{"name":"awssagemaker","arn":"arn:aws:iam::XXXXXXXXXXX:role/sm-execution","container_repo":"XXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/XXXXXXXXXXX"}],"resources":{"process":"ml.t3.medium","train":"ml.m5.large","deploy":"ml.t2.medium"},"metadata":[{"name":"mlflow","tracking_uri":"XXXXXXXXXXX"}]}' --metadata '{"project": "height_data", "job_type": "process"}' --data '{"input":"s3://mlctltest/example1_data/","output":"s3://mlctltest/example1_output/"}'
```