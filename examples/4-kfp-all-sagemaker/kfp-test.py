from mlctl.kfp import dsl, step, run_pipeline
import yaml

@dsl.pipeline
def mlctl_pipeline():    

    input_data ='s3://mlctltest/example1_data/'
    with open('provider.yaml') as f:
        provider = yaml.safe_load(f)

    # with open('provider_mix.yaml') as f:
    #     provider = yaml.safe_load(f)

    # returns a S3 bucket with the processed data
    op1 = step.process(provider=provider, name='sk_learn.process', input=input_data)

    # returns a model artifact
    op2 = step.train(provider=provider, name='sk_learn.train', input=op1.output)

    # creates endpoint, ends pipeline
    op3 = step.deploy(provider=provider, name='sk_learn.deploy', input=op2.output)

    op2.after(op1)
    op3.after(op2)

# change the host to where you want to submit the job
run_pipeline(mlctl_pipeline, host='http://localhost:8080')
